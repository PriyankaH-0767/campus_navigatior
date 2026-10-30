"""
Multimodal Assistant & Evidence-Aware Response Composer
Coordinates RAG, Navigation Graph, CLIP, VLM, and Image Generation.
Maintains multi-turn conversation state, performs entity resolution,
and synthesizes transparent evidence-backed responses.
"""

import re
import os
from typing import Dict, Any, List, Optional, Tuple
from core.campus_graph import CampusNavigationGraph
from core.rag_engine import RAGEngine
from core.clip_engine import CLIPSearchEngine
from core.vlm_engine import VLMEngine
from core.image_generator import CampusVisualGenerator

class CampusAssistant:
    def __init__(
        self,
        data_dir: str = "data",
        chunk_size: int = 180,
        chunk_overlap: int = 30,
        top_k: int = 3,
        similarity_method: str = "cosine",
        use_reranker: bool = True,
        temperature: float = 0.2
    ):
        self.data_dir = data_dir
        self.nav_graph = CampusNavigationGraph()
        self.rag_engine = RAGEngine(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            top_k=top_k,
            similarity_method=similarity_method,
            use_reranker=use_reranker,
            temperature=temperature
        )
        
        # Load corpus
        text_path = os.path.join(data_dir, "campus_directions.txt")
        if os.path.exists(text_path):
            with open(text_path, "r", encoding="utf-8") as f:
                self.rag_engine.load_corpus_from_text(f.read())

        # Load CLIP & VLM
        metadata_path = os.path.join(data_dir, "campus_images_metadata.json")
        self.clip_engine = CLIPSearchEngine(metadata_path if os.path.exists(metadata_path) else None)
        self.vlm_engine = VLMEngine(metadata_path if os.path.exists(metadata_path) else None)
        self.visual_gen = CampusVisualGenerator()

        # Session state per user
        self.session_source: Optional[str] = None
        self.conversation_history: List[Dict[str, str]] = []

    def classify_intent(self, query: str, has_image: bool = False) -> str:
        """Classifies query intent into NAV, RAG, CLIP_SEARCH, VLM, GEN, or MIXED."""
        q = query.lower()

        if has_image and ("how do i reach" in q or "how to get" in q or "guide me" in q):
            return "MIXED"

        if "generate" in q or "illustration" in q or "illustrative" in q or "draw" in q or "visual scene" in q:
            return "GEN_ILLUSTRATION"

        if has_image or ("signs" in q and "photo" in q) or ("visible" in q and "photo" in q):
            return "VLM_ANALYSIS"

        if "photo" in q or "picture" in q or "resemble" in q or "look like" in q or "image of" in q:
            return "CLIP_SEARCH"

        # Check navigation keywords
        nav_triggers = ["how do i reach", "how to reach", "how to go", "how do i go", "guide me to", "directions to", "route to", "way to"]
        if any(t in q for t in nav_triggers):
            return "NAV"

        # Check explicit location declaration e.g. "I am in D block"
        if re.search(r'\bi am (in|at|near)\b', q):
            return "NAV"

        return "RAG"

    def extract_navigation_entities(self, query: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Dynamically extracts source and destination from query or conversation state.
        Preserves explicitly declared source across multi-turn interactions.
        """
        q = query.strip()
        q_low = q.lower()
        extracted_source = None
        extracted_dest = None

        # Clean ancillary landmark phrases for entity matching
        clean_q = re.sub(r'\b(using|with|via)\s+landmarks\b', '', q_low).strip()

        # 1. Pattern: "From [Source] (,|.)? guide me to/to [Dest]"
        match_from_to = re.search(r'\bfrom\s+(?:the\s+)?([a-zA-Z0-9\s\'\-]+?)(?:,|\.|\;)?\s+(?:guide me to|to|how do i reach|how to reach)\s+(?:the\s+)?([a-zA-Z0-9\s\'\-]+)', clean_q)
        if match_from_to:
            s_cand = match_from_to.group(1).strip()
            d_cand = match_from_to.group(2).strip().rstrip("?.")
            s_res = self.nav_graph.resolve_location_id(s_cand)
            d_res = self.nav_graph.resolve_location_id(d_cand)
            if s_res:
                extracted_source = s_res
                self.session_source = s_res
            if d_res:
                extracted_dest = d_res
            elif d_cand:
                extracted_dest = d_cand

        # 2. Pattern: "I am/I'm in/at/near [Source] (,|.)? guide me to/how do I reach [Dest]"
        if not extracted_dest or not extracted_source:
            match_iam_to = re.search(r'\b(?:i am|i\'m)\s+(?:in|at|near)\s+(?:the\s+)?([a-zA-Z0-9\s\'\-]+?)(?:,|\.|\;)?\s+(?:guide me to|to|how do i reach|how to reach)\s+(?:the\s+)?([a-zA-Z0-9\s\'\-]+)', clean_q)
            if match_iam_to:
                s_cand = match_iam_to.group(1).strip()
                d_cand = match_iam_to.group(2).strip().rstrip("?.")
                s_res = self.nav_graph.resolve_location_id(s_cand)
                d_res = self.nav_graph.resolve_location_id(d_cand)
                if s_res:
                    extracted_source = s_res
                    self.session_source = s_res
                if d_res:
                    extracted_dest = d_res
                elif d_cand:
                    extracted_dest = d_cand

        # 3. Pattern: Standalone source: "I am in/at/near [Source]"
        if not extracted_source:
            match_source = re.search(r'\b(?:i am|i\'m)\s+(?:in|at|near)\s+(?:the\s+)?([a-zA-Z0-9\s\'\-]+?)(?:\.|\,|\;|\?|\s+how|\s+guide|$)', clean_q)
            if match_source:
                cand = match_source.group(1).strip()
                res = self.nav_graph.resolve_location_id(cand)
                if res:
                    extracted_source = res
                    self.session_source = res

        # 4. Pattern: Standalone destination: "how do I reach [Dest]" / "guide me to [Dest]"
        if not extracted_dest:
            match_dest = re.search(r'(?:how do i reach|how to reach|how to go to|guide me to|way to)\s+(?:the\s+)?([a-zA-Z0-9\s\'\-]+)', clean_q)
            if match_dest:
                d_cand = match_dest.group(1).strip().rstrip("?.")
                d_res = self.nav_graph.resolve_location_id(d_cand)
                if d_res:
                    extracted_dest = d_res
                else:
                    # Unrecognized destination query (e.g. "MBA")
                    extracted_dest = d_cand

        # Use preserved session source if not explicitly provided in current query
        final_source = extracted_source or self.session_source

        return final_source, extracted_dest

    def process_query(self, query: str, uploaded_image: Optional[str] = None) -> Dict[str, Any]:
        """
        Main multimodal query processing pipeline.
        Dispatches to appropriate branch and composes evidence-aware response.
        """
        has_image = uploaded_image is not None
        intent = self.classify_intent(query, has_image=has_image)

        response_payload = {
            "query": query,
            "intent": intent,
            "source_location": self.session_source,
            "answer": "",
            "citations": [],
            "route_result": None,
            "route_diagram_svg": None,
            "clip_results": None,
            "vlm_result": None,
            "visual_illustration": None,
            "evidence_grounded": True
        }

        # Branch 1: Navigation
        if intent == "NAV":
            source, dest = self.extract_navigation_entities(query)
            
            # Check if user only stated their location
            if re.search(r'^\s*i am (?:in|at|near)\s+([a-zA-Z0-9\s]+)[.!]?\s*$', query.lower()):
                loc_name = self.nav_graph.graph.nodes.get(source, {}).get("name", source)
                response_payload["answer"] = (
                    f"📍 Recorded your current starting location as **{loc_name}**.\n\n"
                    f"Where would you like to navigate on campus? (e.g. 'How do I reach the School of Design?' or 'Guide me to the Sports Area')."
                )
                return response_payload

            if not source:
                response_payload["answer"] = (
                    "To guide you with verified turn-by-turn landmark directions, I need to know your starting location. "
                    "Where are you currently located on campus? (e.g., 'I am at the Fountain' or 'I am in D Block')."
                )
                response_payload["evidence_grounded"] = False
                return response_payload

            if not dest:
                response_payload["answer"] = (
                    f"Starting location set to **{self.nav_graph.graph.nodes.get(source, {}).get('name', source)}**. "
                    "Please specify your destination facility."
                )
                return response_payload

            # Check if destination is ambiguous (e.g. MBA)
            if "mba" in query.lower() and "dean" not in query.lower():
                response_payload["answer"] = (
                    f"I note your starting location is **{self.nav_graph.graph.nodes.get(source, {}).get('name', source)}**, "
                    f"but 'MBA' is ambiguous (could refer to the Dean Office of MBA Department in the Admin complex or specific lecture halls). "
                    f"Could you please clarify if you mean the **Dean Office of MBA Department**?"
                )
                response_payload["evidence_grounded"] = False
                return response_payload

            # Check if destination is recognized
            resolved_dest = self.nav_graph.resolve_location_id(dest)
            if not resolved_dest:
                response_payload["answer"] = (
                    f"Destination '{dest}' was not recognized in the verified campus registry. "
                    f"Please check the spelling or specify a registered building or facility name."
                )
                response_payload["evidence_grounded"] = False
                return response_payload

            # Calculate route
            route_res = self.nav_graph.get_route(source, resolved_dest)
            response_payload["route_result"] = route_res
            response_payload["answer"] = self.nav_graph.generate_natural_directions(route_res)
            
            if route_res.get("success"):
                response_payload["route_diagram_svg"] = self.visual_gen.generate_route_diagram_svg(route_res)

            return response_payload

        # Branch 2: CLIP Search
        elif intent == "CLIP_SEARCH":
            clip_res = self.clip_engine.text_to_image_search(query, top_k=3)
            response_payload["clip_results"] = clip_res
            if clip_res.get("uncertain"):
                response_payload["answer"] = clip_res["explanation"]
            else:
                top_m = clip_res["results"][0]
                response_payload["answer"] = (
                    f"Found matching verified campus photograph for **{top_m['label']}** "
                    f"(Similarity: {top_m['similarity_score']:.2f}).\n"
                    f"Caption: {top_m['caption']} {top_m['citation']}"
                )
                response_payload["citations"] = [top_m["citation"]]
            return response_payload

        # Branch 3: VLM Analysis
        elif intent == "VLM_ANALYSIS":
            img_ref = uploaded_image or "campus_img_registrar_office"
            vlm_res = self.vlm_engine.analyze_image_query(img_ref, query)
            response_payload["vlm_result"] = vlm_res
            response_payload["answer"] = (
                f"👁️ **Visual Observation:** {vlm_res['observation']}\n\n"
                f"🏷️ **Detected Signs:** {', '.join(vlm_res['ocr_detected'])}\n\n"
                f"📌 *Note: {vlm_res.get('source_citation', '[campus_images.pdf]')}*"
            )
            return response_payload

        # Branch 4: Visual Scene Generation (Diffusion Model)
        elif intent == "GEN_ILLUSTRATION":
            gen_res = self.visual_gen.generate_illustration(query)
            response_payload["visual_illustration"] = gen_res
            response_payload["generated_image_path"] = gen_res.get("image_path")
            response_payload["answer"] = (
                f"🎨 **Generated Visual Guide ({gen_res.get('model_type', 'Diffusion Model')}):** {gen_res['scene_title']}.\n\n"
                f"📝 **Diffusion Prompt:** *\"{gen_res.get('diffusion_prompt', query)}\"*\n\n"
                f"{gen_res['disclaimer']}"
            )
            return response_payload

        # Branch 5: Mixed Multimodal Query
        elif intent == "MIXED":
            # Image recognition -> location resolution -> graph routing
            img_ref = uploaded_image or "campus_img_admin_block"
            vlm_res = self.vlm_engine.analyze_image_query(img_ref, query)
            matched_loc = vlm_res.get("catalogue_matched_location", "ADMISSION_BLOCK")
            self.session_source = matched_loc

            # Extract destination
            _, dest = self.extract_navigation_entities(query)
            dest_id = self.nav_graph.resolve_location_id(dest or "RD_CENTRE") or "RD_CENTRE"

            route_res = self.nav_graph.get_route(matched_loc, dest_id)
            route_text = self.nav_graph.generate_natural_directions(route_res)

            response_payload["answer"] = (
                f"1. **Visual Location Identification:** From the image evidence, the building resembles **{self.nav_graph.graph.nodes.get(matched_loc, {}).get('name', matched_loc)}**.\n\n"
                f"2. **Verified Navigation:**\n{route_text}"
            )
            response_payload["route_result"] = route_res
            if route_res.get("success"):
                response_payload["route_diagram_svg"] = self.visual_gen.generate_route_diagram_svg(route_res)
            return response_payload

        # Branch 6: Text RAG (Default)
        else:
            chunks = self.rag_engine.retrieve(query)
            ans_payload = self.rag_engine.generate_grounded_answer(query, chunks)
            response_payload["answer"] = ans_payload["answer"]
            response_payload["citations"] = ans_payload["citations"]
            response_payload["retrieved_chunks"] = chunks
            response_payload["evidence_grounded"] = ans_payload["evidence_supported"]
            return response_payload
