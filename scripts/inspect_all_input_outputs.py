import sys
import os
import json

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.multimodal_assistant import CampusAssistant

def run_inspection():
    assistant = CampusAssistant()

    cases = [
        {
            "category": "1. Factual Text Q&A (RAG)",
            "query": "Which floor is the School of Design on?",
            "image": None,
            "engine": "RAGEngine + SentenceTransformer / TF-IDF Vector Index",
            "model_details": "all-MiniLM-L6-v2 embeddings + Cosine Similarity + Reciprocal Rank Fusion"
        },
        {
            "category": "2. Multi-Hop Campus Knowledge (RAG)",
            "query": "Which food stalls are opposite the Admission Block?",
            "image": None,
            "engine": "RAGEngine + Corpus Citation Extractor",
            "model_details": "Sliding window chunking (180 words) + Page Citation [campus_directions.pdf, Page 1]"
        },
        {
            "category": "3. Direct Navigation (Deterministic Graph)",
            "query": "From the fountain, guide me to the School of Law using landmarks.",
            "image": None,
            "engine": "CampusNavigationGraph (NetworkX)",
            "model_details": "Dijkstra Shortest Path on verified pedestrian graph (100% path validity, 0% hallucination)"
        },
        {
            "category": "4. Multi-Turn Navigation (Turn 1: Origin Declaration)",
            "query": "I am in D Block.",
            "image": None,
            "engine": "CampusAssistant Context State Manager",
            "model_details": "Extracts entity 'D_BLOCK', commits to session_source, asks user for destination"
        },
        {
            "category": "5. Multi-Turn Navigation (Turn 2: Destination using Stored Origin)",
            "query": "How do I reach the School of Design?",
            "image": None,
            "engine": "CampusNavigationGraph + Session State",
            "model_details": "Uses stored session_source (D_BLOCK) -> solves route to SCHOOL_OF_DESIGN (Vertical transition)"
        },
        {
            "category": "6. Ambiguity Resolution (Dean Office vs Classrooms)",
            "query": "How do I reach MBA?",
            "image": None,
            "engine": "CampusAssistant Entity Disambiguation",
            "model_details": "Intercepts ambiguous acronym 'MBA' -> prompts user to clarify if they mean Dean's Office"
        },
        {
            "category": "7. Hallucination Prevention (Unregistered Target)",
            "query": "How do I reach Hogwarts Castle?",
            "image": None,
            "engine": "CampusNavigationGraph Entity Verifier",
            "model_details": "Rejects unmapped destination -> abstains safely instead of fabricating routes"
        },
        {
            "category": "8. Image Visual QA & Sign Reading (VLM + OCR)",
            "query": "What signs are visible in this photo?",
            "image": "office_of_the_registrar.jpg",
            "engine": "VLMEngine (Vision-Language Model)",
            "model_details": "OCR bounding boxes + visual feature extraction + catalogue cross-referencing"
        },
        {
            "category": "9. Visual Appearance Search (CLIP)",
            "query": "Show me a photo of the sports area",
            "image": None,
            "engine": "CLIPSearchEngine (Text-to-Image)",
            "model_details": "Dual-encoder semantic vector projection (threshold tau=0.35 rejection)"
        },
        {
            "category": "10. Mixed Multimodal (Photo Recognition + Landmark Navigation)",
            "query": "From this photo, identify the building and guide me to the Research and Development Centre.",
            "image": "admin_block.jpg",
            "engine": "VLMEngine + CampusNavigationGraph + CampusVisualGenerator",
            "model_details": "VLM identifies Admin Block -> NetworkX routes 110m to R&D Centre -> SVG route map"
        },
        {
            "category": "11. Generative Visual Scene (Diffusion Model)",
            "query": "Generate an illustration of the campus entrance",
            "image": None,
            "engine": "CampusVisualGenerator (Diffusion Model)",
            "model_details": "Prompt conditioning + High-res Diffusion synthesis + Mandatory Safety Watermark banner"
        },
        {
            "category": "12. Out-of-Domain Abstention (Safety Fallback)",
            "query": "What is the capital of Australia and how to bake bread?",
            "image": None,
            "engine": "RAGEngine Strict Grounding Check",
            "model_details": "Low cosine score (<0.05) threshold -> abstains from hallucinating non-campus facts"
        }
    ]

    print("\n" + "="*80)
    print("🔬 COMPREHENSIVE OUTPUT GENERATION AUDIT: ALL INPUT MODALITIES & MODELS")
    print("="*80 + "\n")

    for idx, c in enumerate(cases, 1):
        print(f"--------------------------------------------------------------------------------")
        print(f"CASE {idx}: {c['category']}")
        print(f"  📌 Query:      \"{c['query']}\"")
        if c['image']:
            print(f"  🖼️ Image:      \"{c['image']}\"")
        print(f"  ⚙️ Engine:     {c['engine']}")
        print(f"  🧠 Model Tech: {c['model_details']}")
        
        res = assistant.process_query(c['query'], uploaded_image=c['image'])
        
        print(f"\n  🎯 INTERNAL CLASSIFICATION:")
        print(f"     - Detected Intent: {res.get('intent')}")
        print(f"     - Evidence Grounded: {res.get('evidence_grounded')}")
        if res.get('citations'):
            print(f"     - Citations: {res.get('citations')}")
        if res.get('source_location'):
            print(f"     - Session Source State: {res.get('source_location')}")
        if res.get('route_result') and res['route_result'].get('success'):
            r = res['route_result']
            print(f"     - Route: {' -> '.join(r['route'])}")
            print(f"     - Total Walking Distance: {r['total_distance_m']}m across {len(r['steps'])} segments")
            print(f"     - Landmarks: {', '.join(r.get('landmarks', []))}")
        if res.get('clip_results'):
            top = res['clip_results']['results'][0]
            print(f"     - CLIP Best Match: {top['label']} (Similarity: {top['similarity_score']})")
        if res.get('vlm_result'):
            v = res['vlm_result']
            print(f"     - VLM Detected OCR: {v.get('ocr_detected')}")
            print(f"     - VLM Location ID: {v.get('catalogue_matched_location')}")
        if res.get('visual_illustration'):
            vi = res['visual_illustration']
            print(f"     - Diffusion Prompt: \"{vi.get('diffusion_prompt')}\"")
            print(f"     - Safety Disclaimer: {vi.get('disclaimer')[:60]}...")
            print(f"     - Saved Image: {vi.get('image_path')}")

        print(f"\n  💬 FINAL GENERATED OUTPUT:")
        for line in res['answer'].strip().split("\n"):
            print(f"     {line}")
        print()

if __name__ == "__main__":
    run_inspection()
