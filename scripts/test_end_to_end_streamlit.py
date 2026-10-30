"""
End-to-End Verification Test Script for Streamlit Chatbot & Campus Navigator
Validates:
1. Text Input Queries (RAG with Citations)
2. Image Input Queries (VLM Sign Recognition & CLIP Identification)
3. Mixed Multimodal Queries (Image + Navigation)
4. Navigation Queries (NetworkX Deterministic Routing)
5. Multi-turn State Preservation
6. Diffusion Image Generation
"""

import sys
import os

# Set UTF-8 encoding for console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath("."))

from core.multimodal_assistant import CampusAssistant

def run_tests():
    print("=" * 70)
    print("🧪 RUNNING END-TO-END STREAMLIT ENGINE AUDIT")
    print("=" * 70)

    assistant = CampusAssistant()
    passed = 0
    total = 0

    # -------------------------------------------------------------
    # TEST 1: TEXT INPUT (RAG WITH EXACT CITATION)
    # -------------------------------------------------------------
    total += 1
    q1 = "Which floor is the School of Design on?"
    print(f"\n[TEST 1] Text Input Query: '{q1}'")
    r1 = assistant.process_query(q1)
    ans1 = r1["answer"]
    cits1 = r1["citations"]
    print(f"  Response: {ans1}")
    print(f"  Citations: {cits1}")
    if "fifth floor" in ans1.lower() and "d block" in ans1.lower() and cits1:
        print("  --> [PASS] Correct floor and page citation retrieved.")
        passed += 1
    else:
        print("  --> [FAIL] Incorrect answer.")

    # -------------------------------------------------------------
    # TEST 2: TEXT INPUT (FOOD STALLS OPPOSITE ADMISSION BLOCK)
    # -------------------------------------------------------------
    total += 1
    q2 = "Which food stalls are opposite the Admission Block?"
    print(f"\n[TEST 2] Text Input Query: '{q2}'")
    r2 = assistant.process_query(q2)
    ans2 = r2["answer"]
    print(f"  Response: {ans2}")
    if all(k.lower() in ans2.lower() for k in ["Subway", "Hatti Kaapi", "Aromas of Malenadu", "Taj Delight"]):
        print("  --> [PASS] All 4 food stalls correctly retrieved.")
        passed += 1
    else:
        print("  --> [FAIL] Missing food stalls.")

    # -------------------------------------------------------------
    # TEST 3: IMAGE AS INPUT (PHOTO RECOGNITION & VLM OCR)
    # -------------------------------------------------------------
    total += 1
    img_name = "office_of_the_registrar.jpg"
    q3 = "What signs are visible in this photo?"
    print(f"\n[TEST 3] Image Input: '{img_name}' | Question: '{q3}'")
    r3 = assistant.process_query(q3, uploaded_image=img_name)
    ans3 = r3["answer"]
    ocr_detected = r3["vlm_result"]["ocr_detected"]
    print(f"  Detected Signs: {ocr_detected}")
    print(f"  VLM Output:\n{ans3}")
    if any("OFFICE OF THE REGISTRAR" in s for s in ocr_detected) and "Counter" in str(ocr_detected):
        print("  --> [PASS] Signs accurately read and grounded in catalogue.")
        passed += 1
    else:
        print("  --> [FAIL] Sign OCR detection failed.")

    # -------------------------------------------------------------
    # TEST 4: MIXED MULTIMODAL (PHOTO IDENTIFICATION + NAVIGATION)
    # -------------------------------------------------------------
    total += 1
    img_admin = "admin_block.jpg"
    q4 = "From this photo, identify the building and guide me to the Research and Development Centre."
    print(f"\n[TEST 4] Mixed Multimodal: Photo '{img_admin}' + Query: '{q4}'")
    r4 = assistant.process_query(q4, uploaded_image=img_admin)
    ans4 = r4["answer"]
    route4 = r4.get("route_result")
    print(f"  Assistant Output:\n{ans4}")
    if route4 and route4.get("success") and route4.get("total_distance_m") > 0:
        print(f"  --> [PASS] Successfully identified building and routed ({route4['total_distance_m']}m).")
        passed += 1
    else:
        print("  --> [FAIL] Mixed multimodal navigation failed.")

    # -------------------------------------------------------------
    # TEST 5: DETERMINISTIC NAVIGATION (FOUNTAIN -> SCHOOL OF LAW)
    # -------------------------------------------------------------
    total += 1
    q5 = "From the fountain, guide me to the School of Law using landmarks."
    print(f"\n[TEST 5] Navigation Query: '{q5}'")
    r5 = assistant.process_query(q5)
    ans5 = r5["answer"]
    route5 = r5.get("route_result")
    print(f"  Response:\n{ans5}")
    if route5 and route5.get("success") and len(route5["steps"]) > 0:
        # Check that edges exist in graph
        r_nodes = route5["route"]
        all_edges_valid = all(assistant.nav_graph.graph.has_edge(r_nodes[i], r_nodes[i+1]) for i in range(len(r_nodes)-1))
        if all_edges_valid:
            print(f"  --> [PASS] 100% Valid Path with {len(r_nodes)} waypoints (~{route5['total_distance_m']}m).")
            passed += 1
        else:
            print("  --> [FAIL] Non-existent edge in route!")
    else:
        print("  --> [FAIL] Route calculation failed.")

    # -------------------------------------------------------------
    # TEST 6: MULTI-TURN CONVERSATION STATE & AMBIGUITY HANDLING
    # -------------------------------------------------------------
    total += 1
    print("\n[TEST 6] Multi-Turn Conversation State Test:")
    # Turn 1: Declare starting location
    t1_q = "I am in D Block."
    print(f"  Turn 1: '{t1_q}'")
    assistant.process_query(t1_q)
    stored_src = assistant.session_source
    print(f"    -> Preserved session_source: {stored_src}")

    # Turn 2: Query ambiguous destination "MBA"
    t2_q = "How do I reach MBA?"
    print(f"  Turn 2: '{t2_q}'")
    r_t2 = assistant.process_query(t2_q)
    print(f"    -> Assistant: {r_t2['answer']}")

    # Turn 3: Query destination "School of Design" (inside same building D Block)
    t3_q = "How do I reach the School of Design?"
    print(f"  Turn 3: '{t3_q}'")
    r_t3 = assistant.process_query(t3_q)
    print(f"    -> Assistant: {r_t3['answer']}")

    if stored_src == "D_BLOCK" and "clarify" in r_t2["answer"].lower() and "5th floor" in r_t3["answer"].lower():
        print("  --> [PASS] Multi-turn state maintained; ambiguous destination properly prompted.")
        passed += 1
    else:
        print("  --> [FAIL] Multi-turn state failed.")

    # -------------------------------------------------------------
    # TEST 7: DIFFUSION IMAGE GENERATION WITH SAFETY WATERMARK
    # -------------------------------------------------------------
    total += 1
    q7 = "Generate an illustration of the campus entrance."
    print(f"\n[TEST 7] Generative Visual Query: '{q7}'")
    r7 = assistant.process_query(q7)
    img_path = r7.get("generated_image_path")
    print(f"  Response: {r7['answer']}")
    print(f"  Generated File: {img_path}")
    if img_path and os.path.exists(img_path) and "illustrative" in r7["answer"].lower():
        print("  --> [PASS] Diffusion image generated with safety disclaimer.")
        passed += 1
    else:
        print("  --> [FAIL] Image generation failed.")

    # -------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print(f"🎯 AUDIT RESULT: {passed}/{total} TESTS PASSED ({(passed/total)*100:.1f}%)")
    print("=" * 70)
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    if not success:
        sys.exit(1)
