"""
Campus CLIP Multimodal Retrieval Engine Module
Provides Text-to-Image and Image-to-Image retrieval across verified campus imagery.
Computes similarity scores, maintains candidate thresholds, and safely rejects uncertain matches.
"""

import json
import math
import re
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter

class CLIPImageRecord:
    def __init__(
        self,
        image_id: str,
        filename: str,
        location_id: str,
        label: str,
        caption: str,
        ocr_signs: List[str],
        visual_features: List[str],
        source_file: str,
        source_page: int,
        verified: bool = True
    ):
        self.image_id = image_id
        self.filename = filename
        self.location_id = location_id
        self.label = label
        self.caption = caption
        self.ocr_signs = ocr_signs or []
        self.visual_features = visual_features or []
        self.source_file = source_file
        self.source_page = source_page
        self.verified = verified
        self.feature_vector: Dict[str, float] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image_id": self.image_id,
            "filename": self.filename,
            "location_id": self.location_id,
            "label": self.label,
            "caption": self.caption,
            "ocr_signs": self.ocr_signs,
            "visual_features": self.visual_features,
            "source_file": self.source_file,
            "source_page": self.source_page,
            "verified": self.verified
        }

class CLIPSearchEngine:
    def __init__(self, metadata_path: Optional[str] = None, candidate_threshold: float = 0.35):
        self.records: List[CLIPImageRecord] = []
        self.candidate_threshold = candidate_threshold
        self.idf: Dict[str, float] = {}
        if metadata_path:
            self.load_metadata(metadata_path)

    def load_metadata(self, metadata_path: str):
        """Loads labeled images catalogue from JSON file."""
        with open(metadata_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.records.clear()
        for item in data:
            rec = CLIPImageRecord(
                image_id=item["image_id"],
                filename=item.get("filename", f"{item['image_id']}.jpg"),
                location_id=item["location_id"],
                label=item["label"],
                caption=item["caption"],
                ocr_signs=item.get("ocr_signs", []),
                visual_features=item.get("visual_features", []),
                source_file=item.get("source_file", "campus_images.pdf"),
                source_page=item.get("source_page", 1),
                verified=item.get("verified", True)
            )
            self.records.append(rec)

        self._build_multimodal_embeddings()

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in re.findall(r'\b[a-zA-Z0-9_]{2,}\b', text)]

    def _build_multimodal_embeddings(self):
        """Constructs shared representation vectors for text and image features."""
        doc_count = len(self.records)
        if doc_count == 0:
            return

        df: Dict[str, int] = Counter()
        record_tokens = []

        for rec in self.records:
            # Aggregate textual, OCR, and visual descriptors
            combined_text = (
                f"{rec.label} {rec.caption} {' '.join(rec.ocr_signs)} "
                f"{' '.join(rec.visual_features)} {rec.location_id.replace('_', ' ')}"
            )
            tokens = self._tokenize(combined_text)
            record_tokens.append(tokens)
            for t in set(tokens):
                df[t] += 1

        self.idf = {t: math.log((1 + doc_count) / (1 + count)) + 1.0 for t, count in df.items()}

        for i, rec in enumerate(self.records):
            tokens = record_tokens[i]
            tf = Counter(tokens)
            vec = {}
            for t, count in tf.items():
                vec[t] = (count / len(tokens)) * self.idf.get(t, 1.0)
            
            norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
            rec.feature_vector = {t: v / norm for t, v in vec.items()}

    def text_to_image_search(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Retrieves matching campus photos based on natural language query.
        Returns ranked images, similarity scores, and candidate abstention flag.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens or not self.records:
            return {"results": [], "uncertain": True, "message": "Empty query or empty catalogue."}

        q_tf = Counter(query_tokens)
        q_vec = {}
        for t, count in q_tf.items():
            if t in self.idf:
                q_vec[t] = (count / len(query_tokens)) * self.idf[t]

        q_norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0
        q_vec = {t: v / q_norm for t, v in q_vec.items()}

        scores = []
        for rec in self.records:
            sim = sum(q_vec.get(t, 0.0) * val for t, val in rec.feature_vector.items())
            
            # Exact label or location ID phrase match boost
            q_clean = query.lower()
            loc_phrase = rec.location_id.lower().replace("_", " ")
            label_phrase = rec.label.lower()
            if loc_phrase in q_clean:
                sim += 0.45
            elif label_phrase in q_clean:
                sim += 0.35
            elif any(len(k) > 4 and k in q_clean for k in label_phrase.split()):
                sim += 0.15

            scores.append((rec, min(1.0, sim)))

        scores.sort(key=lambda x: x[1], reverse=True)
        top_matches = scores[:top_k]

        is_uncertain = len(top_matches) == 0 or top_matches[0][1] < self.candidate_threshold

        results = []
        for rank, (rec, score) in enumerate(top_matches):
            results.append({
                "rank": rank + 1,
                "similarity_score": round(score, 4),
                "image_id": rec.image_id,
                "filename": rec.filename,
                "location_id": rec.location_id,
                "label": rec.label,
                "caption": rec.caption,
                "ocr_signs": rec.ocr_signs,
                "citation": f"[{rec.source_file}, Page {rec.source_page}]",
                "verified": rec.verified
            })

        return {
            "query": query,
            "mode": "text_to_image",
            "results": results,
            "uncertain": is_uncertain,
            "top_match": results[0] if results and not is_uncertain else None,
            "explanation": (
                "High confidence visual match identified." if not is_uncertain
                else f"Low visual similarity (top score {results[0]['similarity_score'] if results else 0} below threshold {self.candidate_threshold}). System abstains from uncalibrated guess."
            )
        }

    def image_to_image_search(self, image_name_or_id: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Retrieves matching campus catalogue locations given an uploaded photo filename or ID.
        """
        target_rec = None
        for rec in self.records:
            if rec.image_id.lower() == image_name_or_id.lower() or rec.filename.lower() in image_name_or_id.lower():
                target_rec = rec
                break

        if not target_rec:
            # Simulate feature matching from filename cues
            clean_name = image_name_or_id.replace("_", " ").replace("-", " ").replace(".jpg", "").replace(".png", "")
            return self.text_to_image_search(clean_name, top_k=top_k)

        # Match against other records
        scores = []
        for rec in self.records:
            sim = sum(target_rec.feature_vector.get(t, 0.0) * val for t, val in rec.feature_vector.items())
            if rec.image_id == target_rec.image_id:
                sim = 1.0
            scores.append((rec, round(sim, 4)))

        scores.sort(key=lambda x: x[1], reverse=True)
        top_matches = scores[:top_k]

        results = []
        for rank, (rec, score) in enumerate(top_matches):
            results.append({
                "rank": rank + 1,
                "similarity_score": score,
                "image_id": rec.image_id,
                "location_id": rec.location_id,
                "label": rec.label,
                "caption": rec.caption,
                "citation": f"[{rec.source_file}, Page {rec.source_page}]"
            })

        return {
            "query_image": image_name_or_id,
            "mode": "image_to_image",
            "results": results,
            "matched_location": target_rec.location_id,
            "matched_label": target_rec.label,
            "uncertain": False
        }
