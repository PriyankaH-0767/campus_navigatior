"""
Script to generate all 9 Google Colab notebooks for Smart Campus Explorer AI.
Creates valid .ipynb JSON structures with runnable code cells, markdown descriptions,
and evaluation charts.
"""

import json
import os

def create_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "language_info": {"name": "python"},
            "colab": {"provenance": []}
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

def md_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True)
    }

def code_cell(code):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code.splitlines(keepends=True)
    }

def main():
    target_dir = "Smart_Campus_Explorer"
    os.makedirs(target_dir, exist_ok=True)

    # 01_setup_and_config.ipynb
    nb01 = create_notebook([
        md_cell("# 01. Setup and Environment Configuration\n### Smart Campus Explorer AI\nInitialize libraries, environment settings, and parameter registry."),
        code_cell("""# Install core dependencies
!pip install -q -U openai pymupdf sentence-transformers faiss-cpu networkx transformers pillow pandas scikit-learn matplotlib plotly

import os
import sys
import json
import networkx as nx
import pandas as pd
import numpy as np

print(f"NetworkX Version: {nx.__version__}")
print(f"Pandas Version: {pd.__version__}")
print("Setup complete and ready for Smart Campus Explorer modules!")"""),
        code_cell("""# Configuration Parameters
CONFIG = {
    "chunk_size": 180,
    "chunk_overlap": 30,
    "top_k": 3,
    "similarity_method": "cosine",
    "use_reranker": True,
    "clip_threshold": 0.35,
    "temperature": 0.2
}
print("Active Configuration:")
print(json.dumps(CONFIG, indent=2))""")
    ])
    with open(os.path.join(target_dir, "01_setup_and_config.ipynb"), "w", encoding="utf-8") as f:
        json.dump(nb01, f, indent=2)

    # 02_pdf_ingestion.ipynb
    nb02 = create_notebook([
        md_cell("# 02. PDF Ingestion & Structured Knowledge Extraction\nExtracts text facts, page citations, and labeled campus images."),
        code_cell("""# Load and parse campus directions corpus
campus_text = \"\"\"[Page 1]
from fountain take right
if you take first left you reach "udaya upahara"
if youn take second left you find engineering block and their beside that is the admission block ,in the same building in the first floor you can find "office of registrar" .
if you go inside the engineering block you find h , j ,k and it leads to n, p, q,r,s,u blocks.
if you take exact straight path after left from fountain in the right side you find food stalls opposite to admission block such as 'Subway' , "hatti kaapi", "araomas of malenadu" , "taj delight". 

[Page 2]
if head straight from admission block to find the "d block " near the "stationary" , if take left from from d block you lead to e , f, l blocks , in the left you find e and f block seminar halls. In ground floor  and in first floor of e block you find the "research and development centre" 
in d block fifth floor is the "School of design" .
if you walk into the food stalls you find a way to sports area in the right side, basket ball court, throw ball court and the volley ball court and football courts and the sports room.

[Page 3]
f block leads to l block ,in l block in you left again their are food stalls "hatti kaapi", "v mart", "crazy cups', "lassi area", first floor has dean office .
these food stalls can also be found when you come from n to p , in p block right side.
p leads to q and then r and s ,u  blocks. s block 5th floor you find "School of law".\"\"\"

print("Ingested Campus Directions Corpus:")
print(f"Total length: {len(campus_text)} characters across 3 pages.")"""),
        code_cell("""# Inspect extracted labeled images metadata
sample_image_record = {
    "image_id": "campus_img_registrar_office",
    "file_path": "campus_images/office_of_the_registrar.jpg",
    "location_id": "REGISTRAR_OFFICE",
    "label": "Office of registrar",
    "caption": "First floor Admission Block facility showing blue OFFICE OF THE REGISTRAR sign",
    "ocr_signs": ["OFFICE OF THE REGISTRAR", "Counter-01", "Counter-02", "Counter-03"],
    "source_file": "campus_images.pdf",
    "source_page": 6,
    "verified": True
}
print("Structured Image Record Format:")
print(json.dumps(sample_image_record, indent=2))""")
    ])
    with open(os.path.join(target_dir, "02_pdf_ingestion.ipynb"), "w", encoding="utf-8") as f:
        json.dump(nb02, f, indent=2)

    # 03_rag_experiments.ipynb
    nb03 = create_notebook([
        md_cell("# 03. RAG Experiments: Embeddings, Chunking & Retrieval\nEvaluates chunk sizes (100, 180, 300 words), top-k, similarity metrics, and reranking."),
        code_cell("""from core.rag_engine import RAGEngine

# Compare chunk sizes: 100 vs 180 vs 300
experiments = [
    {"name": "Small Chunks", "chunk_size": 100, "chunk_overlap": 15},
    {"name": "Medium Chunks (Default)", "chunk_size": 180, "chunk_overlap": 30},
    {"name": "Large Chunks", "chunk_size": 300, "chunk_overlap": 50}
]

for exp in experiments:
    engine = RAGEngine(chunk_size=exp["chunk_size"], chunk_overlap=exp["chunk_overlap"])
    engine.load_corpus_from_text(campus_text)
    print(f"{exp['name']}: Total indexed chunks = {len(engine.chunks)}")"""),
        code_cell("""# Run test query
test_query = "Which floor is the School of Design on?"
retrieved = engine.retrieve(test_query, top_k=3)
ans = engine.generate_grounded_answer(test_query, retrieved)

print(f"Query: {test_query}")
print(f"Answer: {ans['answer']}")
print(f"Citations: {ans['citations']}")""")
    ])
    with open(os.path.join(target_dir, "03_rag_experiments.ipynb"), "w", encoding="utf-8") as f:
        json.dump(nb03, f, indent=2)

    # 04_campus_graph.ipynb
    nb04 = create_notebook([
        md_cell("# 04. Deterministic Campus Graph Navigation\nConstructs verified NetworkX graph, calculates shortest routes, and synthesizes landmark directions."),
        code_cell("""from core.campus_graph import CampusNavigationGraph

nav = CampusNavigationGraph()
print(f"Nodes in campus graph: {len(nav.graph.nodes)}")
print(f"Traversable edges: {len(nav.graph.edges)}")

# Test verified route from Fountain to School of Law
route_res = nav.get_route("FOUNTAIN", "SCHOOL_OF_LAW")
print(f"Success: {route_res['success']}")
print(f"Total Walking Distance: {route_res['total_distance_m']}m")
print(\"\\n\" + nav.generate_natural_directions(route_res))"""),
        code_cell("""# Test non-existent path rejection (Zero-Hallucination)
fake_res = nav.get_route("FOUNTAIN", "NON_EXISTENT_BUILDING")
print(f"Handled missing destination: {fake_res['error']}")""")
    ])
    with open(os.path.join(target_dir, "04_campus_graph.ipynb"), "w", encoding="utf-8") as f:
        json.dump(nb04, f, indent=2)

    # 05_clip_image_search.ipynb
    nb05 = create_notebook([
        md_cell("# 05. CLIP Multimodal Image Exploration\nText-to-Image and Image-to-Image retrieval across verified campus photos."),
        code_cell("""from core.clip_engine import CLIPSearchEngine

clip = CLIPSearchEngine("data/campus_images_metadata.json")
# Text to image query
q = "Find a photo of D Block"
t2i_res = clip.text_to_image_search(q, top_k=3)

print(f"Query: '{q}'")
for r in t2i_res["results"]:
    print(f"Rank {r['rank']}: {r['label']} (Similarity: {r['similarity_score']}) {r['citation']}")"""),
        code_cell("""# Test uncertain match abstention
unk_res = clip.text_to_image_search("A photo of an alien spaceship on Mars", top_k=3)
print(f"Uncertain: {unk_res['uncertain']}")
print(f"Abstention explanation: {unk_res['explanation']}")""")
    ])
    with open(os.path.join(target_dir, "05_clip_image_search.ipynb"), "w", encoding="utf-8") as f:
        json.dump(nb05, f, indent=2)

    # 06_vlm_experiments.ipynb
    nb06 = create_notebook([
        md_cell("# 06. Vision-Language Model (VLM) Experiments\nVisual feature extraction, OCR sign reading, and catalogue verification."),
        code_cell("""from core.vlm_engine import VLMEngine

vlm = VLMEngine("data/campus_images_metadata.json")
res = vlm.analyze_image_query("campus_img_registrar_office", "What signs are visible in this photo?")

print(f"Observation: {res['observation']}")
print(f"Detected Signs: {res['ocr_detected']}")
print(f"Grounded Location: {res['catalogue_matched_location']}")""")
    ])
    with open(os.path.join(target_dir, "06_vlm_experiments.ipynb"), "w", encoding="utf-8") as f:
        json.dump(nb06, f, indent=2)

    # 07_image_generation.ipynb
    nb07 = create_notebook([
        md_cell("# 07. Visual Explanation & Image Generation\nGenerates illustrative scenes with mandatory watermarks and verified route diagrams."),
        code_cell("""from core.image_generator import CampusVisualGenerator

gen = CampusVisualGenerator()
scene = gen.generate_illustration("Generate an illustration of the campus entrance.")

print(f"Title: {scene['scene_title']}")
print(f"Disclaimer: {scene['disclaimer']}")
print("SVG Data Generated (ready to render in HTML/Streamlit).")""")
    ])
    with open(os.path.join(target_dir, "07_image_generation.ipynb"), "w", encoding="utf-8") as f:
        json.dump(nb07, f, indent=2)

    # 08_integrated_assistant.ipynb
    nb08 = create_notebook([
        md_cell("# 08. Integrated Multimodal Campus Assistant\nUnifies RAG, Navigation Graph, CLIP, VLM, and Image Gen with multi-turn conversation state."),
        code_cell("""from core.multimodal_assistant import CampusAssistant

assistant = CampusAssistant()

# Multi-turn interaction test
print("--- Turn 1 ---")
r1 = assistant.process_query("I am in D Block.")
print(r1["answer"])

print(\"\\n--- Turn 2 ---\")
r2 = assistant.process_query("How do I reach the School of Design?")
print(r2["answer"])

print(\"\\n--- Turn 3: Ambiguous destination ---\")
r3 = assistant.process_query("How do I reach MBA?")
print(r3["answer"])""")
    ])
    with open(os.path.join(target_dir, "08_integrated_assistant.ipynb"), "w", encoding="utf-8") as f:
        json.dump(nb08, f, indent=2)

    # 09_evaluation.ipynb
    nb09 = create_notebook([
        md_cell("# 09. Comprehensive Evaluation & Ablations (A1 to A8)\nRuns ground-truth benchmarking on test cases and logs ablation metrics."),
        code_cell("""from core.multimodal_assistant import CampusAssistant
from core.evaluator import CampusEvaluator
import pandas as pd

assistant = CampusAssistant()
evaluator = CampusEvaluator(assistant)

print("Running Full Ground-Truth Evaluation...")
bench = evaluator.run_benchmark()
print(\"\\n--- Benchmark Summary Metrics ---\")
for k, v in bench["metrics"].items():
    print(f"{k}: {v}")

print(\"\\n--- Ablation Studies A1 to A8 ---\")
ablations = evaluator.run_ablations()
df_ab = pd.DataFrame(ablations)[["id", "name", "baseline_score", "comparison_score"]]
print(df_ab.to_string(index=False))""")
    ])
    with open(os.path.join(target_dir, "09_evaluation.ipynb"), "w", encoding="utf-8") as f:
        json.dump(nb09, f, indent=2)

    print("All 9 notebooks generated successfully in Smart_Campus_Explorer/")

if __name__ == "__main__":
    main()
