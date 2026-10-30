"""
Smart Campus Explorer AI — Presidency Campus Guide
Multimodal AI Campus Assistant with Interactive Plotly Route Navigation,
Grounded Text RAG, Diffusion Visual Generation, and Domain Sidebars.
"""

import os
import re
import json
import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from PIL import Image

from core.multimodal_assistant import CampusAssistant
from core.evaluator import CampusEvaluator

# Page Configuration
st.set_page_config(
    page_title="Smart Campus Explorer AI • Presidency Guide",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# HIGH-END STYLING (DM Sans, Glassmorphic Cards, Modern Layout)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.stApp {
    background: #F8FAFC;
    color: #0F172A;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1750px;
}
.hero-header {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F766E 100%);
    padding: 1.4rem 1.8rem;
    border-radius: 16px;
    color: white;
    margin-bottom: 1.2rem;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
}
.hero-title {
    font-size: 1.85rem;
    font-weight: 800;
    color: #FFFFFF;
    margin: 0;
    letter-spacing: -0.02em;
}
.hero-sub {
    font-size: 0.95rem;
    color: #94A3B8;
    margin-top: 0.35rem;
    margin-bottom: 0.8rem;
}
.badge-verified {
    background: #10B981;
    color: white;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    display: inline-block;
    margin-right: 6px;
}
.badge-rag {
    background: #0EA5E9;
    color: white;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    display: inline-block;
    margin-right: 6px;
}
.badge-diffusion {
    background: #8B5CF6;
    color: white;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
    display: inline-block;
}
.panel-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.2rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    margin-bottom: 1.2rem;
}
.citation-pill {
    background: #F1F5F9;
    color: #0369A1;
    border: 1px solid #BAE6FD;
    padding: 2px 7px;
    border-radius: 5px;
    font-size: 0.75rem;
    font-family: monospace;
}
.step-box {
    background: #F8FAFC;
    border-left: 4px solid #10B981;
    padding: 8px 12px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 6px;
    font-size: 0.88rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CAMPUS SCHEMATIC GRAPH & 2D COORDINATES
# Coordinates reflect campus spatial layout for interactive Plotly visualization.
# -----------------------------------------------------------------------------
CAMPUS_COORDINATES = {
    # Central Avenue & Landmarks
    "University Entrance": (50, 4, "Entrance", "Ground", "Main campus entrance gateway"),
    "FOUNTAIN": (50, 32, "Landmark", "Ground", "Central campus landmark & primary navigation anchor"),
    "UDAYA_UPAHARA": (68, 32, "Food", "Ground", "First left turn from fountain; traditional snacks"),
    
    # Engineering & Admission Complex
    "ENGINEERING_BLOCK": (44, 48, "Academic", "Ground", "Houses engineering faculties; connects internally to H-K & N-U"),
    "ADMISSION_BLOCK": (58, 48, "Office", "Ground", "Administration and visitor reception; houses Registrar on 1st Floor"),
    "REGISTRAR_OFFICE": (62, 50, "Office", "1st Floor", "Admission Block 1st floor; student records & admissions"),
    "CONTROLLER_EXAMINATION": (56, 52, "Office", "Ground", "Examination and evaluation counters"),
    
    # Food Stalls
    "FOOD_STALLS_ADMISSION": (44, 40, "Food", "Ground", "Opposite Admission Block: Subway, Hatti Kaapi, Aromas, Taj Delight"),
    "SPORTS_AREA": (28, 28, "Sports", "Ground", "Basketball, volleyball, throwball, football courts, gym, sports room"),
    "DOMINOS": (26, 40, "Food", "Ground", "Outdoor Domino's pizza outlet kiosk"),
    
    # D, E, F, L Academic Wings
    "STATIONERY": (70, 50, "Services", "Ground", "Campus stationery and photocopy supplies near D Block"),
    "D_BLOCK": (76, 54, "Academic", "Ground", "Academic block near stationery; 5th floor houses School of Design"),
    "SCHOOL_OF_DESIGN": (76, 57, "Academic", "5th Floor", "School of Design studios on 5th floor of D Block"),
    "E_BLOCK": (84, 64, "Academic", "Ground", "Left from D Block; E Block seminar hall & R&D Centre"),
    "RD_CENTRE": (86, 65, "Research", "Ground & 1st Floor", "Research & Development Centre on ground & 1st floor of E Block"),
    "F_BLOCK": (84, 72, "Academic", "Ground", "F Block seminar hall; directly connects to L Block"),
    "L_BLOCK": (84, 82, "Academic", "Ground", "Ground floor School of Media Studies; 1st floor Dean's Office"),
    "SCHOOL_OF_MEDIA_STUDIES": (88, 82, "Academic", "Ground", "Media Studies soundstages and TV Studio on L Block ground floor"),
    "DEAN_OFFICE_L_BLOCK": (88, 85, "Office", "1st Floor", "Dean's Office on 1st floor of L Block"),
    "FOOD_STALLS_L_BLOCK": (74, 82, "Food", "Ground", "Food arcade: V Mart, Crazy Cups, Hatti Kaapi, Lassi Area"),
    
    # Engineering Spine (H, J, K -> N, P, Q, R, S, U)
    "H_BLOCK": (44, 58, "Academic", "Ground", "Internal corridor connection inside Engineering Block"),
    "J_BLOCK": (44, 64, "Academic", "Ground", "Internal engineering corridor"),
    "K_BLOCK": (44, 70, "Academic", "Ground", "Connecting passage towards N Block"),
    "N_BLOCK": (52, 75, "Academic", "Ground", "Academic block connector"),
    "P_BLOCK": (58, 80, "Academic", "Ground", "Academic block; food stalls accessible on right side"),
    "Q_BLOCK": (58, 85, "Academic", "Ground", "Corridor connecting P and R blocks"),
    "R_BLOCK": (58, 90, "Academic", "Ground", "Corridor connecting Q and S blocks"),
    "S_BLOCK": (58, 95, "Academic", "Ground", "Academic block; 5th floor houses School of Law"),
    "SCHOOL_OF_LAW": (62, 97, "Academic", "5th Floor", "School of Law faculty and moot court on 5th floor of S Block"),
    "U_BLOCK": (58, 100, "Academic", "Ground", "Terminal academic block in southern spine"),
    
    # Campus Facilities & West Wing
    "CENTRAL_LIBRARY": (35, 52, "Facility", "Ground & 1st", "Multi-storey campus library and reading halls"),
    "CAFETERIA": (24, 52, "Food", "Ground", "Central student cafeteria concourse"),
    "AUDITORIUM": (24, 62, "Facility", "Ground", "Grand campus auditorium and event amphitheater"),
    "DEAN_OFFICE_MBA": (24, 70, "Office", "1st Floor", "Dean Office of MBA Department in Admin / Management complex"),
    "AMPHITHEATER": (38, 44, "Landmark", "Ground", "Open-air amphitheater with landscaped lawn steps")
}

# Domain Category Taxonomy for Sidebar Navigation
DOMAIN_CATEGORIES = {
    "🎓 Academic Blocks & Schools": [
        ("D_BLOCK", "D Block (School of Design on 5th Floor)"),
        ("SCHOOL_OF_DESIGN", "School of Design (D Block Floor 5)"),
        ("S_BLOCK", "S Block (School of Law on 5th Floor)"),
        ("SCHOOL_OF_LAW", "School of Law (S Block Floor 5)"),
        ("ENGINEERING_BLOCK", "Engineering Block (H, J, K Wings)"),
        ("E_BLOCK", "E Block (R&D Centre)"),
        ("F_BLOCK", "F Block (Seminar Hall)"),
        ("L_BLOCK", "L Block (School of Media Studies & Dean Office)"),
        ("SCHOOL_OF_MEDIA_STUDIES", "School of Media Studies / TV Studio"),
        ("N_BLOCK", "N Block"),
        ("P_BLOCK", "P Block"),
        ("Q_BLOCK", "Q Block"),
        ("R_BLOCK", "R Block"),
        ("U_BLOCK", "U Block")
    ],
    "🏛️ Offices & Administration": [
        ("ADMISSION_BLOCK", "Admission Block"),
        ("REGISTRAR_OFFICE", "Office of the Registrar (Admission Block Floor 1)"),
        ("CONTROLLER_EXAMINATION", "Office of Controller of Examination"),
        ("DEAN_OFFICE_MBA", "Dean Office of MBA Department"),
        ("DEAN_OFFICE_L_BLOCK", "Dean's Office (L Block Floor 1)")
    ],
    "☕ Food & Dining Outlets": [
        ("FOOD_STALLS_ADMISSION", "Food Stalls (Subway, Hatti Kaapi, Aromas, Taj Delight)"),
        ("FOOD_STALLS_L_BLOCK", "Food Arcade (V Mart, Crazy Cups, Lassi Area)"),
        ("UDAYA_UPAHARA", "Udaya Upahara (First left from Fountain)"),
        ("CAFETERIA", "Central Cafeteria"),
        ("DOMINOS", "Domino's Pizza Outlet")
    ],
    "🏀 Sports & Campus Facilities": [
        ("SPORTS_AREA", "Sports Complex (Basketball, Volleyball, Football, Gym)"),
        ("CENTRAL_LIBRARY", "Central University Library"),
        ("RD_CENTRE", "Research & Development (R&D) Centre"),
        ("AUDITORIUM", "Main Campus Auditorium"),
        ("AMPHITHEATER", "Open-Air Amphitheater"),
        ("STATIONERY", "Stationery & Photocopy Store")
    ]
}

# -----------------------------------------------------------------------------
# PLOTLY INTERACTIVE MAP BUILDER
# -----------------------------------------------------------------------------
def make_interactive_campus_map(nav_graph: nx.Graph, active_route=None, start_node=None, dest_node=None):
    """
    Renders an interactive 2D schematic campus map using Plotly.
    Highlights confirmed background walkways and active shortest-path route.
    """
    active_route = active_route or []
    fig = go.Figure()

    # 1. Background Walkable Paths (Light Slate Gray)
    for u, v in nav_graph.edges():
        if u in CAMPUS_COORDINATES and v in CAMPUS_COORDINATES:
            xu, yu, _, _, _ = CAMPUS_COORDINATES[u]
            xv, yv, _, _, _ = CAMPUS_COORDINATES[v]
            fig.add_trace(go.Scatter(
                x=[xu, xv], y=[yu, yv],
                mode="lines",
                line=dict(color="#CBD5E1", width=3),
                hoverinfo="skip",
                showlegend=False
            ))

    # 2. Highlighted Route Segments (Vibrant Emerald / Cyan)
    if len(active_route) > 1:
        rx, ry = [], []
        route_hover_texts = []
        for i, node_id in enumerate(active_route):
            if node_id in CAMPUS_COORDINATES:
                x, y, cat, floor, desc = CAMPUS_COORDINATES[node_id]
                rx.append(x)
                ry.append(y)
                route_hover_texts.append(f"<b>Step {i+1}: {node_id.replace('_', ' ')}</b><br>{desc}")

        fig.add_trace(go.Scatter(
            x=rx, y=ry,
            mode="lines+markers",
            line=dict(color="#10B981", width=6),
            marker=dict(size=12, color="#10B981", line=dict(color="#FFFFFF", width=2)),
            name="Verified Route",
            text=route_hover_texts,
            hoverinfo="text"
        ))

    # 3. Campus Location Nodes
    xs, ys, node_names, colors, sizes, hovers = [], [], [], [], [], []
    for node_id, (x, y, category, floor, desc) in CAMPUS_COORDINATES.items():
        xs.append(x)
        ys.append(y)
        clean_name = node_id.replace("_", " ")
        node_names.append(clean_name)
        hovers.append(f"<b>{clean_name}</b><br>🏷️ Category: {category}<br>🏢 Floor: {floor}<br>📝 {desc}")

        if node_id == start_node:
            colors.append("#2563EB")  # Royal Blue for Start
            sizes.append(20)
        elif node_id == dest_node:
            colors.append("#DC2626")  # Crimson Red for Destination
            sizes.append(20)
        elif node_id in active_route:
            colors.append("#10B981")  # Emerald for Route Waypoints
            sizes.append(14)
        else:
            colors.append("#64748B")  # Muted Slate for others
            sizes.append(10)

    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="markers+text",
        marker=dict(size=sizes, color=colors, line=dict(color="#FFFFFF", width=1.5)),
        text=node_names,
        textposition="top center",
        textfont=dict(size=9, color="#0F172A", family="Plus Jakarta Sans"),
        hovertext=hovers,
        hoverinfo="text",
        showlegend=False
    ))

    fig.update_layout(
        height=520,
        margin=dict(l=15, r=15, t=15, b=15),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F8FAFC",
        xaxis=dict(visible=False, range=[15, 95], fixedrange=True),
        yaxis=dict(visible=False, range=[0, 108], fixedrange=True, scaleanchor="x"),
        hoverlabel=dict(bgcolor="#0F172A", font_size=11, font_color="#FFFFFF"),
        showlegend=False
    )
    return fig

# -----------------------------------------------------------------------------
# INITIALIZE ASSISTANT ENGINE
# -----------------------------------------------------------------------------
if "assistant" not in st.session_state:
    st.session_state.assistant = CampusAssistant()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Welcome to **Smart Campus Explorer AI**! I am your multimodal campus guide.\n\n"
                       "Ask me about any building, floor location, food stall, navigate to any facility with verified landmarks, "
                       "upload photos for visual recognition, or request conceptual architectural illustrations.",
            "citations": ["[campus_directions.pdf, Page 1]"],
            "route_result": None,
            "generated_image": None
        }
    ]

if "last_route" not in st.session_state:
    st.session_state.last_route = None

if "last_gen_image" not in st.session_state:
    st.session_state.last_gen_image = None

assistant = st.session_state.assistant

# -----------------------------------------------------------------------------
# SIDEBAR: CLICKABLE DOMAINS, ROUTE SELECTOR & CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧭 Quick Route Planner")
    st.caption("Select locations from the dropdowns to compute verified paths:")

    node_keys = sorted(list(CAMPUS_COORDINATES.keys()))
    start_default_idx = node_keys.index("FOUNTAIN") if "FOUNTAIN" in node_keys else 0
    dest_default_idx = node_keys.index("SCHOOL_OF_LAW") if "SCHOOL_OF_LAW" in node_keys else 1

    sb_start = st.selectbox("📍 Starting Point", options=node_keys, index=start_default_idx, format_func=lambda x: x.replace("_", " "))
    sb_dest = st.selectbox("🎯 Destination", options=node_keys, index=dest_default_idx, format_func=lambda x: x.replace("_", " "))

    if st.button("🚀 Calculate Verified Route", type="primary", use_container_width=True):
        route_calc = assistant.nav_graph.get_route(sb_start, sb_dest)
        st.session_state.last_route = route_calc
        assistant.session_source = sb_start
        st.session_state.messages.append({
            "role": "user",
            "content": f"How do I reach {sb_dest.replace('_', ' ')} from {sb_start.replace('_', ' ')}?"
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant.nav_graph.generate_natural_directions(route_calc),
            "citations": ["[campus_directions.pdf]"],
            "route_result": route_calc,
            "generated_image": None
        })
        st.rerun()

    st.markdown("---")
    st.markdown("### 🏫 Clickable Campus Domains")
    st.caption("Browse registered facilities by category:")

    for category_name, facilities in DOMAIN_CATEGORIES.items():
        with st.expander(category_name, expanded=False):
            for fid, fname in facilities:
                col_btn1, col_btn2 = st.columns([7, 3])
                with col_btn1:
                    st.markdown(f"**{fname}**")
                with col_btn2:
                    if st.button("Route ➔", key=f"btn_nav_{fid}", help=f"Set as destination"):
                        current_s = assistant.session_source or "FOUNTAIN"
                        route_calc = assistant.nav_graph.get_route(current_s, fid)
                        st.session_state.last_route = route_calc
                        st.session_state.messages.append({
                            "role": "user",
                            "content": f"Guide me to {fname}"
                        })
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": assistant.nav_graph.generate_natural_directions(route_calc),
                            "citations": ["[campus_directions.pdf]"],
                            "route_result": route_calc,
                            "generated_image": None
                        })
                        st.rerun()

    st.markdown("---")
    st.markdown("### ⚙️ Experimental Parameters")
    with st.expander("🛠️ Retrieval & Model Controls", expanded=False):
        chunk_size = st.select_slider("RAG Chunk Size (words)", options=[100, 180, 300], value=180)
        top_k = st.slider("Top-k Retrieval", min_value=1, max_value=5, value=3)
        sim_method = st.selectbox("Similarity Metric", ["cosine", "dot_product"], index=0)
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

        assistant.rag_engine.chunk_size = chunk_size
        assistant.rag_engine.top_k = top_k
        assistant.rag_engine.similarity_method = sim_method
        assistant.rag_engine.temperature = temperature

    st.markdown("---")
    st.markdown("### 📊 Benchmark & Evaluation")
    if st.button("▶️ Run Automated Audit (16 Tests)", use_container_width=True):
        evaluator = CampusEvaluator(assistant)
        eval_res = evaluator.run_benchmark()
        st.success(f"Audit Complete! Overall Accuracy: {eval_res['metrics']['overall_accuracy']*100:.1f}% | Path Validity: {eval_res['metrics']['nav_path_validity']*100:.1f}%")

    if st.button("🔄 Reset Chat & Location", use_container_width=True):
        assistant.session_source = None
        st.session_state.messages = st.session_state.messages[:1]
        st.session_state.last_route = None
        st.session_state.last_gen_image = None
        st.rerun()

# -----------------------------------------------------------------------------
# MAIN INTERFACE: HERO HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🧭 Smart Campus Explorer AI • Presidency Guide</div>
    <div class="hero-sub">Multimodal Campus Assistant • Grounded PDF RAG • Verified Landmark Navigation • Diffusion Generative Visuals</div>
    <div>
        <span class="badge-verified">✅ 100% Path Validity Guaranteed</span>
        <span class="badge-rag">📄 Grounded PDF RAG</span>
        <span class="badge-diffusion">🎨 Diffusion Scene Synthesis</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TWO-COLUMN LAYOUT: CHATBOT INTERFACE (LEFT) & LIVE OUTPUT WINDOW (RIGHT)
# -----------------------------------------------------------------------------
col_chat, col_output = st.columns([5, 6], gap="medium")

# ==================== LEFT COLUMN: CHATBOT UI ====================
with col_chat:
    st.markdown("#### 💬 Multimodal Campus Chatbot")

    # Quick prompt pills
    st.caption("💡 Quick prompts to try:")
    qp_cols = st.columns(3)
    with qp_cols[0]:
        if st.button("Floor of Design?", use_container_width=True):
            st.session_state.active_query = "Which floor is the School of Design on?"
    with qp_cols[1]:
        if st.button("Fountain ➔ Law", use_container_width=True):
            st.session_state.active_query = "From the fountain, guide me to the School of Law using landmarks."
    with qp_cols[2]:
        if st.button("Entrance Visual", use_container_width=True):
            st.session_state.active_query = "Generate an illustration of the campus entrance"

    # Chat Messages Scroll Area
    chat_container = st.container(height=450)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("citations"):
                    st.markdown(" ".join([f"<span class='citation-pill'>{c}</span>" for c in msg["citations"]]), unsafe_allow_html=True)
                if msg.get("generated_image") and os.path.exists(msg["generated_image"]):
                    st.image(msg["generated_image"], caption="🎨 Diffusion Generated Visual Aid", use_container_width=True)

    # Image File Uploader
    uploaded_photo = st.file_uploader("📷 Upload a campus photo or map snippet (Optional)", type=["jpg", "jpeg", "png"], key="uploader_main")
    uploaded_name = uploaded_photo.name if uploaded_photo else None
    if uploaded_photo:
        st.info(f"Photo attached: **{uploaded_name}**")

    # Chat Input Box
    query_input = st.chat_input("Ask about buildings, floors, food stalls, routes, or request illustrations...")

    if "active_query" in st.session_state and st.session_state.active_query:
        query_input = st.session_state.active_query
        st.session_state.active_query = None

    if query_input:
        # Append User Message
        st.session_state.messages.append({"role": "user", "content": query_input})

        # Process Query with Multimodal Assistant Engine
        with st.spinner("Processing campus query..."):
            resp = assistant.process_query(query_input, uploaded_image=uploaded_name)

        if resp.get("route_result"):
            st.session_state.last_route = resp["route_result"]
        if resp.get("generated_image_path"):
            st.session_state.last_gen_image = resp["generated_image_path"]

        st.session_state.messages.append({
            "role": "assistant",
            "content": resp["answer"],
            "citations": resp.get("citations", []),
            "route_result": resp.get("route_result"),
            "generated_image": resp.get("generated_image_path")
        })
        st.rerun()

# ==================== RIGHT COLUMN: OUTPUT WINDOW & VISUALS ====================
with col_output:
    st.markdown("#### 🗺️ Live Output Window & Navigation Visualizer")

    # Render Interactive Plotly Campus Map
    active_route_nodes = []
    start_point = assistant.session_source
    dest_point = None

    if st.session_state.last_route and st.session_state.last_route.get("success"):
        active_route_nodes = st.session_state.last_route.get("route", [])
        start_point = st.session_state.last_route.get("source")
        dest_point = st.session_state.last_route.get("destination")

    plotly_fig = make_interactive_campus_map(
        assistant.nav_graph.graph,
        active_route=active_route_nodes,
        start_node=start_point,
        dest_node=dest_point
    )
    st.plotly_chart(plotly_fig, use_container_width=True, config={"displayModeBar": False})

    # Output Card 1: Turn-by-Turn Guidance if route is active
    if st.session_state.last_route and st.session_state.last_route.get("success"):
        r_data = st.session_state.last_route
        with st.container():
            st.markdown(f"##### 🚶 Verified Route Guidance (~{r_data['total_distance_m']}m walking distance)")
            for s in r_data.get("steps", []):
                landmark_info = f" • *Landmark: {s['landmark']}*" if s.get('landmark') else ""
                vertical_info = " 🛗 [Elevator/Stairs]" if s.get('is_vertical') else ""
                st.markdown(f"<div class='step-box'><b>Step {s['step_number']}:</b> {s['instruction']}{landmark_info}{vertical_info}</div>", unsafe_allow_html=True)

    # Output Card 2: Generated Diffusion Visual Aid if available
    elif st.session_state.last_gen_image and os.path.exists(st.session_state.last_gen_image):
        with st.container():
            st.markdown("##### 🎨 Diffusion Generative Campus Visual Aid")
            st.image(st.session_state.last_gen_image, caption="⚠️ Illustrative Conceptual Visual Aid — Not Verified Route Geometry", use_container_width=True)

    # Output Card 3: Default Campus Directory Overview
    else:
        with st.container():
            st.markdown("##### 🏛️ Verified Campus Reference Facts")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                st.markdown("""
                - **D Block (Floor 5):** School of Design
                - **S Block (Floor 5):** School of Law
                - **E Block (Ground & 1):** R&D Centre
                - **Admission Block (Floor 1):** Registrar Office
                """)
            with col_f2:
                st.markdown("""
                - **L Block (Ground):** Media Studies
                - **L Block (Floor 1):** Dean's Office
                - **Food Arcade:** Subway, Hatti Kaapi, Aromas, Taj Delight
                - **Sports Complex:** Basketball, Volleyball, Football, Gym
                """)
