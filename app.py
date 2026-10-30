"""
CampusDrive — Presidency AI Campus Assistant
Clean, unified multimodal campus guide with interactive 2D route map,
semantic text Q&A, Google Gemini vision analysis, and illustrative visual generation.
"""

import os
import re
import json
import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from PIL import Image

from core.multimodal_assistant import CampusAssistant

# Page Configuration
st.set_page_config(
    page_title="CampusDrive — Presidency Campus Assistant",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# HIGH-CONTRAST ACCESSIBLE STYLING (Guaranteed Zero Black Boxes & Uniform Text)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Force clean light theme and high-contrast dark text universally */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}

/* Ensure ALL markdown, paragraphs, headings, list items are 100% visible */
p, span, label, div.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown li, .stMarkdown strong {
    color: #0F172A !important;
    font-weight: 500;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1750px;
}

/* Hero Header */
.hero-header {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 55%, #0284C7 100%) !important;
    padding: 1.4rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.2rem;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.12);
}
.hero-title, .hero-title * {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    margin: 0;
    letter-spacing: -0.02em;
}
.hero-sub, .hero-sub * {
    font-size: 0.95rem !important;
    color: #E2E8F0 !important;
    margin-top: 0.35rem;
    margin-bottom: 0.6rem;
}

/* Status Badges */
.badge-nav { background: #10B981 !important; color: #FFFFFF !important; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; display: inline-block; margin-right: 6px; }
.badge-vlm { background: #0284C7 !important; color: #FFFFFF !important; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; display: inline-block; margin-right: 6px; }
.badge-rag { background: #8B5CF6 !important; color: #FFFFFF !important; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.75rem; display: inline-block; }

/* Streamlit Chat Messages: High visibility card */
[data-testid="stChatMessage"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    margin-bottom: 10px !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03) !important;
}
[data-testid="stChatMessage"] * {
    color: #0F172A !important;
}
[data-testid="stChatMessage"] p {
    color: #0F172A !important;
    font-size: 0.96rem !important;
    line-height: 1.6 !important;
}

/* Step Boxes for Navigation */
.step-box {
    background: #FFFFFF !important;
    border-left: 5px solid #10B981 !important;
    border-top: 1px solid #E2E8F0 !important;
    border-right: 1px solid #E2E8F0 !important;
    border-bottom: 1px solid #E2E8F0 !important;
    padding: 12px 16px !important;
    border-radius: 0 8px 8px 0 !important;
    margin-bottom: 8px !important;
    font-size: 0.92rem !important;
    line-height: 1.5 !important;
    color: #0F172A !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
}
.step-box * {
    color: #0F172A !important;
}

/* Citation Pill */
.citation-pill {
    background: #E0F2FE !important;
    color: #0369A1 !important;
    border: 1px solid #BAE6FD !important;
    padding: 3px 8px !important;
    border-radius: 6px !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    font-family: monospace !important;
    display: inline-block !important;
    margin-top: 4px !important;
}

/* Active Image Context Banner */
.active-photo-card {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* OVERRIDE ALL DARK/BLACK WIDGET BOXES */
div[data-baseweb="select"] > div,
div[data-baseweb="select"] input,
div[data-baseweb="select"] span {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
}
div[data-baseweb="popover"] div,
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
}
li[role="option"]:hover, li[aria-selected="true"] {
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
}

/* File Uploader styling */
[data-testid="stFileUploader"] {
    background-color: #FFFFFF !important;
    border: 2px dashed #93C5FD !important;
    border-radius: 12px !important;
    padding: 12px !important;
}
[data-testid="stFileUploader"] section {
    background-color: #F8FAFC !important;
}
[data-testid="stFileUploader"] section * {
    color: #334155 !important;
}

/* Chat Input Bar */
[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06) !important;
}
[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    font-size: 0.95rem !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #64748B !important;
}

/* Buttons */
button[kind="primary"] {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
button[kind="secondary"] {
    background-color: #FFFFFF !important;
    color: #1E293B !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
button[kind="secondary"]:hover {
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
    border-color: #93C5FD !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #F1F5F9 !important;
}
[data-testid="stSidebar"] * {
    color: #0F172A !important;
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

# Key landmark anchors displayed permanently without text overlap
PRIMARY_LANDMARKS = {
    "FOUNTAIN", "University Entrance", "ENGINEERING_BLOCK", "ADMISSION_BLOCK",
    "D_BLOCK", "SCHOOL_OF_DESIGN", "SCHOOL_OF_LAW", "SPORTS_AREA",
    "CENTRAL_LIBRARY", "AUDITORIUM", "L_BLOCK", "RD_CENTRE", "FOOD_STALLS_ADMISSION"
}

# -----------------------------------------------------------------------------
# PLOTLY INTERACTIVE MAP BUILDER (Clean, Non-Overlapping Labels)
# -----------------------------------------------------------------------------
def make_interactive_campus_map(nav_graph: nx.Graph, active_route=None, start_node=None, dest_node=None):
    """
    Renders an interactive 2D schematic campus map using Plotly.
    Displays clear, non-overlapping labels only for major landmarks and active route waypoints.
    """
    active_route = active_route or []
    fig = go.Figure()

    # 1. Background Walkable Paths (Slate Gray)
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

    # 2. Highlighted Route Segments (Vibrant Emerald)
    if len(active_route) > 1:
        rx, ry = [], []
        route_hover_texts = []
        for i, node_id in enumerate(active_route):
            if node_id in CAMPUS_COORDINATES:
                x, y, cat, floor, desc = CAMPUS_COORDINATES[node_id]
                rx.append(x)
                ry.append(y)
                route_hover_texts.append(f"<b>Segment {i+1}: {node_id.replace('_', ' ')}</b><br>{desc}")

        fig.add_trace(go.Scatter(
            x=rx, y=ry,
            mode="lines+markers",
            line=dict(color="#10B981", width=6),
            marker=dict(size=14, color="#10B981", line=dict(color="#FFFFFF", width=2)),
            name="Verified Route",
            text=route_hover_texts,
            hoverinfo="text"
        ))

    # 3. Campus Location Nodes & Selective Labels
    xs, ys, display_labels, colors, sizes, hovers = [], [], [], [], [], []
    for node_id, (x, y, category, floor, desc) in CAMPUS_COORDINATES.items():
        xs.append(x)
        ys.append(y)
        clean_name = node_id.replace("_", " ")
        hovers.append(f"<b>{clean_name}</b><br>🏷️ Category: {category}<br>🏢 Floor: {floor}<br>📝 {desc}")

        # Selective label logic to prevent visual text clumping
        if node_id == start_node:
            colors.append("#2563EB")  # Blue for Start
            sizes.append(22)
            display_labels.append(f"📍 START: {clean_name}")
        elif node_id == dest_node:
            colors.append("#DC2626")  # Red for Destination
            sizes.append(22)
            display_labels.append(f"🎯 DEST: {clean_name}")
        elif node_id in active_route:
            colors.append("#10B981")  # Emerald for Active Path
            sizes.append(15)
            step_idx = active_route.index(node_id) + 1
            display_labels.append(f"#{step_idx} {clean_name}")
        elif node_id in PRIMARY_LANDMARKS:
            colors.append("#475569")  # Dark Slate for Primary Landmarks
            sizes.append(12)
            display_labels.append(clean_name)
        else:
            colors.append("#94A3B8")  # Subtle Slate for intermediate dots
            sizes.append(9)
            display_labels.append("")  # Blank label prevents visual collisions

    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="markers+text",
        marker=dict(size=sizes, color=colors, line=dict(color="#FFFFFF", width=2)),
        text=display_labels,
        textposition="top center",
        textfont=dict(size=10, color="#0F172A", family="Plus Jakarta Sans"),
        hovertext=hovers,
        hoverinfo="text",
        showlegend=False
    ))

    fig.update_layout(
        height=540,
        margin=dict(l=15, r=15, t=15, b=15),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F8FAFC",
        xaxis=dict(visible=False, range=[15, 95], fixedrange=True),
        yaxis=dict(visible=False, range=[0, 108], fixedrange=True, scaleanchor="x"),
        hoverlabel=dict(bgcolor="#0F172A", font_size=12, font_color="#FFFFFF"),
        showlegend=False
    )
    return fig

# -----------------------------------------------------------------------------
# INITIALIZE ASSISTANT ENGINE & CONVERSATION STATE
# -----------------------------------------------------------------------------
if "assistant" not in st.session_state:
    st.session_state.assistant = CampusAssistant()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Welcome to **CampusDrive**! I am your AI campus guide.\n\n"
                       "You can:\n"
                       "• **Ask campus questions:** buildings, floors, food stalls, faculties, and facilities.\n"
                       "• **Get verified directions:** enter your starting point and destination for landmark guidance.\n"
                       "• **Upload or choose a campus photo:** I will identify the building, read visible signs, show nearest landmarks, and let you ask follow-up questions.\n"
                       "• **Request visual illustrations:** ask to generate an illustrative scene of any campus facility.",
            "citations": ["[campus_directions.pdf, Page 1]"],
            "route_result": None,
            "generated_image": None
        }
    ]

if "last_route" not in st.session_state:
    st.session_state.last_route = None

if "last_gen_image" not in st.session_state:
    st.session_state.last_gen_image = None

if "active_image" not in st.session_state:
    st.session_state.active_image = None

assistant = st.session_state.assistant

# -----------------------------------------------------------------------------
# SIDEBAR: QUICK ROUTE PLANNER, DIRECTORY & GEMINI KEY
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧭 Quick Route Planner")
    st.caption("Select origin and destination to compute verified paths:")

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
    st.markdown("### 🏫 Campus Directory")
    st.caption("Browse registered facilities by domain:")

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
    st.markdown("### 🤖 Google Gemini Vision")
    gemini_key_input = st.text_input(
        "🔑 Gemini API Key (Optional)",
        type="password",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="Provide your Google Gemini API key to activate live Gemini 2.5 Flash Multimodal Vision."
    )
    if gemini_key_input:
        st.session_state["gemini_api_key"] = gemini_key_input
        assistant.vlm_engine.api_key = gemini_key_input

    st.markdown("---")
    if st.button("🔄 New Conversation", use_container_width=True):
        assistant.session_source = None
        st.session_state.active_image = None
        st.session_state.messages = st.session_state.messages[:1]
        st.session_state.last_route = None
        st.session_state.last_gen_image = None
        st.rerun()

# -----------------------------------------------------------------------------
# MAIN INTERFACE: HERO HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🧭 CampusDrive</div>
    <div class="hero-sub">Intelligent Campus Guide • Verified Landmark Navigation • Multimodal Vision Assistant</div>
    <div>
        <span class="badge-nav">🚶 Verified Navigation</span>
        <span class="badge-vlm">👁️ Multimodal Vision</span>
        <span class="badge-rag">📄 Grounded Campus Facts</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TWO-COLUMN LAYOUT: CHATBOT INTERFACE (LEFT) & LIVE OUTPUT WINDOW (RIGHT)
# -----------------------------------------------------------------------------
col_chat, col_output = st.columns([5, 6], gap="medium")

# ==================== LEFT COLUMN: CHATBOT UI ====================
with col_chat:
    st.markdown("#### 💬 CampusDrive Assistant")

    # Quick prompt pills
    st.caption("💡 Suggested questions:")
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
                if msg.get("uploaded_image") and os.path.exists(msg["uploaded_image"]):
                    st.image(msg["uploaded_image"], caption=f"📷 {os.path.basename(msg['uploaded_image'])}", width=260)
                st.markdown(msg["content"])
                if msg.get("citations"):
                    st.markdown(" ".join([f"<span class='citation-pill'>{c}</span>" for c in msg["citations"]]), unsafe_allow_html=True)
                if msg.get("generated_image") and os.path.exists(msg["generated_image"]):
                    st.image(msg["generated_image"], caption="🎨 Illustrative Visual Aid", use_container_width=True)

    # ACTIVE IMAGE BANNER & MULTIMODAL FOLLOW-UP CONTROLS
    if st.session_state.active_image and os.path.exists(st.session_state.active_image):
        with st.container():
            st.markdown("""
            <div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 8px 12px; margin-bottom: 8px;">
                <span style="font-weight: 700; color: #1D4ED8;">🖼️ Active Photo in Focus:</span>
                <span style="color: #1E293B; font-weight: 500;">Ask any follow-up questions about visible signs, doors, floors, or navigate from here!</span>
            </div>
            """, unsafe_allow_html=True)
            col_act1, col_act2, col_act3 = st.columns([2, 5, 3])
            with col_act1:
                st.image(st.session_state.active_image, width=70)
            with col_act2:
                st.markdown(f"**Focus:** `{os.path.basename(st.session_state.active_image)}`")
                if assistant.session_source:
                    loc_label = assistant.nav_graph.graph.nodes.get(assistant.session_source, {}).get("name", assistant.session_source)
                    st.caption(f"📍 Location set to: **{loc_label}**")
            with col_act3:
                if st.button("❌ Remove Photo", use_container_width=True, help="Switch back to text-only mode"):
                    st.session_state.active_image = None
                    st.rerun()

    # Image Input Section: File Uploader or Preset Selection
    sample_photos = {
        "-- Or pick an official campus photo to analyze --": None,
        "🏛️ Admin Block (Main Atrium)": "data/sample_images/admin_block.jpg",
        "📋 Office of the Registrar (Counter Signs)": "data/sample_images/office_of_the_registrar.jpg",
        "🎨 School of Design (D Block Floor 5)": "data/sample_images/school_of_design.jpg",
        "⚖️ School of Law (S Block Floor 5)": "data/sample_images/school_of_law.jpg",
        "🍕 Domino's Pizza Outlet": "data/sample_images/dominos.jpg",
        "📚 Central University Library": "data/sample_images/central_library.jpg",
        "☕ Udaya Upahar (Snacks Landmark)": "data/sample_images/udaya_upahar.jpg",
        "🔬 AI Centre of Excellence": "data/sample_images/ai_centre_of_excellence.jpg",
        "🏀 Indoor Games Hall": "data/sample_images/indoor_games.jpg",
        "🎬 School of Media Studies (TV Studio)": "data/sample_images/media_studies.jpg"
    }

    with st.expander("📷 Upload a Photo or Pick a Campus Landmark Photo", expanded=(st.session_state.active_image is None)):
        uploaded_file = st.file_uploader("Upload your campus photo:", type=["jpg", "jpeg", "png"], key="uploader_widget")
        selected_preset = st.selectbox("Or choose a verified campus photo:", options=list(sample_photos.keys()), index=0)

        new_image_path = None
        if uploaded_file is not None:
            upload_dir = os.path.join("data", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            new_image_path = os.path.join(upload_dir, uploaded_file.name)
            with open(new_image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        elif sample_photos.get(selected_preset):
            new_image_path = sample_photos[selected_preset]

        if new_image_path and os.path.exists(new_image_path) and new_image_path != st.session_state.active_image:
            st.session_state.active_image = new_image_path
            st.success(f"Loaded: {os.path.basename(new_image_path)}")
            # Trigger immediate analysis
            st.session_state.active_query = "Identify this campus photo, read any visible signage, and tell me the nearest landmarks."
            st.rerun()

    # Chat Input Box
    query_input = st.chat_input("Ask about buildings, routes, or ask follow-ups on the active photo...")

    if "active_query" in st.session_state and st.session_state.active_query:
        query_input = st.session_state.active_query
        st.session_state.active_query = None

    if query_input:
        # Append User Message
        active_img = st.session_state.active_image
        st.session_state.messages.append({
            "role": "user",
            "content": query_input,
            "uploaded_image": active_img
        })

        # Process Query with CampusDrive Multimodal Engine
        with st.spinner("CampusDrive is processing your query..."):
            resp = assistant.process_query(
                query_input,
                uploaded_image=active_img,
                api_key=st.session_state.get("gemini_api_key")
            )

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
    st.markdown("#### 🗺️ Interactive Campus Map & Guidance")

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

    # Output Card 1: Turn-by-Turn Guidance if route is active (Distance removed)
    if st.session_state.last_route and st.session_state.last_route.get("success"):
        r_data = st.session_state.last_route
        with st.container():
            st.markdown("##### 🚶 Verified Route Guidance")
            for s in r_data.get("steps", []):
                landmark_info = f" • *Landmark: {s['landmark']}*" if s.get('landmark') else ""
                vertical_info = " 🛗 [Elevator/Stairs]" if s.get('is_vertical') else ""
                st.markdown(f"<div class='step-box'><b>Step {s['step_number']}:</b> {s['instruction']}{landmark_info}{vertical_info}</div>", unsafe_allow_html=True)

    # Output Card 2: Generated Visual Aid if available
    elif st.session_state.last_gen_image and os.path.exists(st.session_state.last_gen_image):
        with st.container():
            st.markdown("##### 🎨 Campus Illustration")
            st.image(st.session_state.last_gen_image, caption="⚠️ Illustrative Conceptual Visual Aid — Not Verified Route Geometry", use_container_width=True)

    # Output Card 3: Default Campus Directory Overview
    else:
        with st.container():
            st.markdown("##### 🏛️ Verified Campus Reference Directory")
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
