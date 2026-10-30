"""
CampusDrive — Presidency AI Campus Assistant
Unified multimodal campus guide with interactive 2D route map,
semantic text Q&A, Google Gemini vision analysis, nearest-location discovery,
and illustrative visual generation.
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

/* Force clean light theme and CSS variables universally regardless of system dark mode */
:root, [data-theme="dark"], [data-theme="light"], .stApp {
    --background-color: #F8FAFC !important;
    --secondary-background-color: #FFFFFF !important;
    --text-color: #0F172A !important;
    --primary-color: #2563EB !important;
    color-scheme: light !important;
}

html, body, [class*="css"], .stApp, .main, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}

/* Force light background on all Streamlit containers */
[data-testid="stAppViewContainer"] > section,
[data-testid="stMain"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[data-testid="stBottom"],
[data-testid="stBottom"] > div {
    background-color: #F8FAFC !important;
}

/* Ensure ALL markdown, paragraphs, headings, list items are 100% visible */
p, span, label, div.stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown li, .stMarkdown strong, .stMarkdown em,
[data-testid="stWidgetLabel"] label, [data-testid="stWidgetLabel"] span {
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
    border: 1px solid #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    margin-bottom: 10px !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04) !important;
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
    border-top: 1px solid #CBD5E1 !important;
    border-right: 1px solid #CBD5E1 !important;
    border-bottom: 1px solid #CBD5E1 !important;
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

/* Quick Action Cards */
.nearest-card {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin-bottom: 8px !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
}

/* OVERRIDE ALL DARK/BLACK WIDGET BOXES (Dropdowns, Inputs, Popovers) */
div[data-testid="stSelectbox"],
div[data-testid="stSelectbox"] > div,
div[data-baseweb="select"],
div[data-baseweb="select"] > div,
div[data-baseweb="select"] div,
div[data-baseweb="select"] input,
div[data-baseweb="select"] span {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
}
div[data-baseweb="select"] > div {
    border: 1.5px solid #94A3B8 !important;
    border-radius: 8px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
div[data-baseweb="select"] svg {
    fill: #0F172A !important;
}
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] span,
ul[role="listbox"],
li[role="option"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
}
li[role="option"]:hover, li[aria-selected="true"] {
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
}

/* Text Inputs (API Key, etc.) */
[data-testid="stTextInput"],
[data-testid="stTextInput"] > div,
[data-testid="stTextInput"] input,
div[data-baseweb="input"],
div[data-baseweb="input"] > div,
div[data-baseweb="input"] input,
div[data-baseweb="base-input"],
div[data-baseweb="base-input"] > div,
div[data-baseweb="base-input"] input {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
}
[data-testid="stTextInput"] input,
div[data-baseweb="input"] > div {
    border: 1.5px solid #94A3B8 !important;
    border-radius: 8px !important;
}

/* File Uploader Dropzone and Children */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] > section,
[data-testid="stFileUploader"] section,
[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploaderDropzone"] > div,
[data-testid="stFileUploaderDropzone"] div,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
section[data-testid="stFileUploadDropzone"],
section[data-testid="stFileUploadDropzone"] div,
section[data-testid="stFileUploadDropzone"] span,
section[data-testid="stFileUploadDropzone"] small {
    background-color: #FFFFFF !important;
    color: #1E293B !important;
}
[data-testid="stFileUploaderDropzone"],
section[data-testid="stFileUploadDropzone"] {
    border: 2px dashed #3B82F6 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stFileUploader"] button,
[data-testid="stFileUploaderDropzone"] button,
section[data-testid="stFileUploadDropzone"] button {
    background: #EFF6FF !important;
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
    border: 1.5px solid #93C5FD !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
[data-testid="stFileUploader"] button:hover,
[data-testid="stFileUploaderDropzone"] button:hover,
section[data-testid="stFileUploadDropzone"] button:hover {
    background: #DBEAFE !important;
    background-color: #DBEAFE !important;
    color: #1E40AF !important;
}

/* Chat Input Bar */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] > div,
[data-testid="stChatInput"] textarea,
[data-testid="stBottom"],
[data-testid="stBottom"] > div {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
}
[data-testid="stChatInput"] {
    border: 2px solid #94A3B8 !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08) !important;
}
[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    font-size: 0.96rem !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #64748B !important;
}
[data-testid="stChatInput"] button {
    background: #2563EB !important;
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
}
[data-testid="stChatInput"] button svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}

/* Buttons (Primary & Secondary) */
.stButton button,
button,
button[data-testid="baseButton-secondary"],
button[kind="secondary"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1.5px solid #94A3B8 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
.stButton button:hover,
button:hover,
button[data-testid="baseButton-secondary"]:hover,
button[kind="secondary"]:hover {
    background: #EFF6FF !important;
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
    border-color: #3B82F6 !important;
}
.stButton button[kind="primary"],
button[data-testid="baseButton-primary"],
button[kind="primary"] {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25) !important;
}
.stButton button[kind="primary"] *,
button[data-testid="baseButton-primary"] *,
button[kind="primary"] * {
    color: #FFFFFF !important;
}

/* Sidebar styling */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child,
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"] {
    background-color: #F1F5F9 !important;
    border-right: 1px solid #E2E8F0 !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] strong {
    color: #0F172A !important;
    font-weight: 600;
}

/* Expanders */
[data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
[data-testid="stExpander"] summary {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    font-weight: 600 !important;
}
[data-testid="stExpander"] summary:hover {
    color: #2563EB !important;
}
[data-testid="stExpander"] > div[role="region"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# UNIFIED CAMPUS 2D COORDINATES (ALL 64 LOCATIONS & WAYPOINTS INTEGRATED)
# -----------------------------------------------------------------------------
CAMPUS_COORDINATES = {
    # 1. Main Entrance & Central Spine
    "UNIVERSITY_ENTRANCE": (50, 4, "Entrance", "Ground", "Main campus entrance gate and palm avenue"),
    "FOUNTAIN": (50, 26, "Landmark", "Ground", "Central campus fountain and primary orientation anchor"),
    "JUNCTION_FOUNTAIN_RIGHT": (50, 32, "Junction", "Ground", "Avenue intersection turning right from fountain"),
    "JUNCTION_FIRST_LEFT": (60, 32, "Junction", "Ground", "First avenue opening towards Udaya Upahar"),
    "UDAYA_UPAHARA": (68, 30, "Food", "Ground", "Traditional breakfast, snacks, and dining outlet"),
    "JUNCTION_SECOND_LEFT": (52, 42, "Junction", "Ground", "Avenue turnoff into Engineering Block portico"),

    # 2. Engineering & Computer Labs Complex
    "ENGINEERING_BLOCK": (44, 46, "Academic", "Ground", "Engineering faculties; internal concourse to H-K wings"),
    "CIVIL_DEPARTMENT": (40, 50, "Academic", "Ground", "Department of Civil Engineering laboratories and classrooms"),
    "COMPUTER_LAB": (38, 56, "Facility", "Ground", "Central university computer laboratory"),
    "FULL_STACK_LAB": (40, 62, "Academic", "Ground", "Full Stack Development and software engineering lab"),
    "AI_CENTRE_OF_EXCELLENCE": (44, 66, "Research", "Ground", "NVIDIA AI Centre of Excellence and research facilities"),
    "VR_STUDIO": (48, 66, "Research", "Ground", "Virtual Reality & Immersive Computing studio"),

    # 3. Admission / Administration Complex & Services
    "ADMISSION_BLOCK": (58, 46, "Office", "Ground", "Administration and admissions reception atrium"),
    "REGISTRAR_OFFICE": (62, 48, "Office", "1st Floor", "Office of the Registrar; admissions and student verification"),
    "CONTROLLER_EXAMINATION": (56, 50, "Office", "Ground", "Office of Controller of Examination service counters"),
    "DEAN_OFFICE_MBA": (54, 44, "Office", "1st Floor", "Dean Office of MBA Department in Admin block"),
    "FEE_DEPARTMENT": (60, 44, "Office", "Ground", "Student fee payments and accounts counter"),
    "OFFICE_INTERNATIONAL_AFFAIRS": (64, 46, "Office", "Ground", "Office of International Affairs and student relations"),
    "CAMPUS_ATM": (64, 40, "Service", "Ground", "24/7 Automated Teller Machine kiosk"),

    # 4. Food Stalls & Dining (Opposite Admin)
    "FOOD_STALLS_ADMISSION": (46, 38, "Food", "Ground", "Food arcade opposite Admin Block: Subway, Hatti Kaapi, Aromas, Taj"),
    "CAFE_FEASTO": (48, 36, "Food", "Ground", "Cafe Feasto fast-food and beverage stall"),
    "HATTI_KAAPI": (44, 36, "Food", "Ground", "Hatti Kaapi traditional filter coffee kiosk"),

    # 5. Sports Complex, Athletics & Domino's
    "JUNCTION_SPORTS_PATH": (36, 32, "Junction", "Ground", "Path branching right towards sports complex"),
    "SPORTS_AREA": (28, 28, "Sports", "Ground", "Basketball, volleyball, football courts and athletic ground"),
    "INDOOR_GAMES": (24, 26, "Sports", "Ground", "Indoor table tennis tournament and board games hall"),
    "GYM": (30, 24, "Sports", "Ground", "Campus student gymnasium and fitness centre"),
    "DOMINOS": (28, 38, "Food", "Ground", "Outdoor Domino's Pizza kiosk"),

    # 6. Central Library, DSA, Cafeteria & Auditorium (West Concourse)
    "CENTRAL_LIBRARY": (34, 48, "Facility", "Ground & 1st", "Central University Library, digital reading rooms & archives"),
    "CAFETERIA": (24, 50, "Food", "Ground", "Central student cafeteria dining hall"),
    "AMPHITHEATER": (36, 42, "Landmark", "Ground", "Open-air landscaped lawn amphitheater"),
    "AUDITORIUM": (24, 60, "Facility", "Ground", "Grand campus auditorium and convocation hall"),
    "DSA_OFFICE": (32, 58, "Office", "Ground", "Directorate of Student Affairs (DSA) office"),
    "MUSICAL_ROOM": (28, 62, "Facility", "Ground", "Cultural musical practice room under canopy"),
    "MEDICAL_ROOM": (38, 52, "Service", "Ground", "Medical Room & Infirmary (Manipal Clinics)"),
    "TRANSPORT_DEPARTMENT": (34, 44, "Office", "Ground", "Bus transport and commuting services office"),
    "M_BLOCK": (36, 68, "Academic", "Ground", "M Block lecture halls and classrooms"),

    # 7. D Block, School of Design & R&D Wing
    "JUNCTION_STATIONERY": (66, 46, "Junction", "Ground", "Connecting walkway from Admin Block to D Block"),
    "STATIONERY": (70, 48, "Service", "Ground", "Stationery, textbooks and photocopy supplies store"),
    "D_BLOCK": (76, 52, "Academic", "Ground", "D Block academic entrance foyer"),
    "SCHOOL_OF_DESIGN": (76, 56, "Academic", "5th Floor", "School of Design studios on 5th floor of D Block"),
    "JUNCTION_D_LEFT": (78, 56, "Junction", "Ground", "West connector walkway from D Block to E Block"),
    "E_BLOCK": (84, 62, "Academic", "Ground", "E Block seminar halls and academic wings"),
    "RD_CENTRE": (86, 64, "Research", "Ground & 1st", "Research & Development Centre, robotics and AI labs"),
    "F_BLOCK": (84, 70, "Academic", "Ground", "F Block seminar hall and lecture rooms"),

    # 8. L Block, Media Studies & Food Arcade (East Spine)
    "NEXUS_CORE": (80, 78, "Junction", "Ground", "Nexus Core central transition underpass and stairwell"),
    "L_BLOCK": (84, 80, "Academic", "Ground", "L Block academic complex"),
    "SCHOOL_OF_MEDIA_STUDIES": (88, 80, "Academic", "Ground", "School of Media Studies soundstages and TV Studio"),
    "DEAN_OFFICE_L_BLOCK": (88, 84, "Office", "1st Floor", "Dean's Office on 1st floor of L Block"),
    "DEAN_OFFICE_PSCS": (88, 87, "Office", "1st Floor", "Dean Office PSCS on 1st floor of L Block"),
    "FOOD_STALLS_L_BLOCK": (74, 80, "Food", "Ground", "Food arcade near L Block: VJ Mart, Crazy Cups, Lassi House"),
    "VJ_MART": (72, 78, "Food", "Ground", "VJ Mart grocery, beverages and student store"),
    "CRAZY_CUPS": (74, 84, "Food", "Ground", "Crazy Cups beverage kiosk"),
    "LASSI_HOUSE": (76, 82, "Food", "Ground", "Lassi House shakes and refreshments stall"),

    # 9. Engineering Internal Concourse (H, J, K -> N, P, Q, R, S, U)
    "H_BLOCK": (44, 54, "Academic", "Ground", "Internal corridor inside Engineering Block"),
    "J_BLOCK": (44, 60, "Academic", "Ground", "Internal engineering academic corridor"),
    "K_BLOCK": (44, 68, "Academic", "Ground", "Internal corridor connecting towards N Block"),
    "N_BLOCK": (52, 72, "Academic", "Ground", "N Block academic wing and pedestrian connector"),
    "P_BLOCK": (58, 78, "Academic", "Ground", "P Block classrooms and food pavilion access"),
    "Q_BLOCK": (58, 84, "Academic", "Ground", "Q Block academic corridor"),
    "R_BLOCK": (58, 88, "Academic", "Ground", "R Block covered walkway"),
    "S_BLOCK": (58, 94, "Academic", "Ground", "S Block main academic entrance"),
    "SCHOOL_OF_LAW": (62, 96, "Academic", "5th Floor", "School of Law faculty and moot court on 5th floor of S Block"),
    "LAW_LIBRARY": (64, 96, "Facility", "5th Floor", "Specialized Law Library on 5th floor of S Block"),
    "U_BLOCK": (58, 100, "Academic", "Ground", "Terminal academic block in south concourse")
}

# Domain Category Taxonomy for Sidebar Navigation
DOMAIN_CATEGORIES = {
    "🎓 Academic Blocks & Faculties": [
        ("D_BLOCK", "D Block (School of Design on Floor 5)"),
        ("SCHOOL_OF_DESIGN", "School of Design (D Block Floor 5)"),
        ("S_BLOCK", "S Block (School of Law on Floor 5)"),
        ("SCHOOL_OF_LAW", "School of Law (S Block Floor 5)"),
        ("LAW_LIBRARY", "Law Library (S Block Floor 5)"),
        ("ENGINEERING_BLOCK", "Engineering Block"),
        ("CIVIL_DEPARTMENT", "Department of Civil Engineering"),
        ("COMPUTER_LAB", "Computer Laboratory"),
        ("FULL_STACK_LAB", "Full Stack Development Lab"),
        ("AI_CENTRE_OF_EXCELLENCE", "AI Centre of Excellence"),
        ("VR_STUDIO", "VR Studio"),
        ("E_BLOCK", "E Block (R&D Centre)"),
        ("RD_CENTRE", "Research & Development Centre"),
        ("F_BLOCK", "F Block (Seminar Hall)"),
        ("L_BLOCK", "L Block (Media Studies)"),
        ("SCHOOL_OF_MEDIA_STUDIES", "School of Media Studies (TV Studio)"),
        ("M_BLOCK", "M Block Classrooms"),
        ("N_BLOCK", "N Block"),
        ("P_BLOCK", "P Block"),
        ("Q_BLOCK", "Q Block"),
        ("R_BLOCK", "R Block"),
        ("U_BLOCK", "U Block")
    ],
    "🏛️ Administration & Student Offices": [
        ("ADMISSION_BLOCK", "Admission Block (Admin)"),
        ("REGISTRAR_OFFICE", "Office of the Registrar (Floor 1)"),
        ("CONTROLLER_EXAMINATION", "Office of Controller of Examination"),
        ("DEAN_OFFICE_MBA", "Dean Office of MBA Department"),
        ("FEE_DEPARTMENT", "Fee Department Counters"),
        ("OFFICE_INTERNATIONAL_AFFAIRS", "Office of International Affairs"),
        ("CAMPUS_ATM", "24/7 Campus ATM"),
        ("DSA_OFFICE", "Directorate of Student Affairs (DSA)"),
        ("TRANSPORT_DEPARTMENT", "Transport Department"),
        ("DEAN_OFFICE_L_BLOCK", "Dean's Office (L Block Floor 1)"),
        ("DEAN_OFFICE_PSCS", "Dean Office PSCS (L Block Floor 1)")
    ],
    "☕ Food Courts & Dining Outlets": [
        ("FOOD_STALLS_ADMISSION", "Food Stalls (Subway, Hatti Kaapi, Aromas, Taj)"),
        ("CAFE_FEASTO", "Cafe Feasto"),
        ("HATTI_KAAPI", "Hatti Kaapi"),
        ("FOOD_STALLS_L_BLOCK", "Food Arcade (VJ Mart, Crazy Cups, Lassi House)"),
        ("VJ_MART", "VJ Mart Store"),
        ("CRAZY_CUPS", "Crazy Cups"),
        ("LASSI_HOUSE", "Lassi House"),
        ("UDAYA_UPAHARA", "Udaya Upahar"),
        ("CAFETERIA", "Central Cafeteria"),
        ("DOMINOS", "Domino's Pizza Outlet")
    ],
    "🏀 Sports, Library & Landmarks": [
        ("FOUNTAIN", "Campus Fountain"),
        ("UNIVERSITY_ENTRANCE", "University Entrance Gate"),
        ("SPORTS_AREA", "Sports Complex (Courts)"),
        ("INDOOR_GAMES", "Indoor Games Hall"),
        ("GYM", "Campus Fitness Gym"),
        ("CENTRAL_LIBRARY", "Central University Library"),
        ("AUDITORIUM", "Main Campus Auditorium"),
        ("AMPHITHEATER", "Open-Air Amphitheater"),
        ("MUSICAL_ROOM", "Musical Practice Room"),
        ("MEDICAL_ROOM", "Medical Infirmary (Manipal Clinics)"),
        ("STATIONERY", "Stationery & Photocopy Shop"),
        ("NEXUS_CORE", "Nexus Core Transition")
    ]
}

# Key landmark anchors displayed permanently with clean non-overlapping labels
PRIMARY_LANDMARKS = {
    "FOUNTAIN", "UNIVERSITY_ENTRANCE", "ENGINEERING_BLOCK", "ADMISSION_BLOCK",
    "D_BLOCK", "SCHOOL_OF_DESIGN", "SCHOOL_OF_LAW", "SPORTS_AREA",
    "CENTRAL_LIBRARY", "AUDITORIUM", "L_BLOCK", "RD_CENTRE",
    "FOOD_STALLS_ADMISSION", "DOMINOS", "UDAYA_UPAHARA"
}

# -----------------------------------------------------------------------------
# PLOTLY SINGLE UNIFIED CAMPUS MAP BUILDER
# -----------------------------------------------------------------------------
def make_interactive_campus_map(nav_graph: nx.Graph, active_route=None, start_node=None, dest_node=None, nearest_nodes=None):
    """
    Renders the single unified 2D schematic campus map with Plotly.
    Connects START and DESTINATION with an active route line and integrates all places.
    """
    active_route = active_route or []
    nearest_nodes = nearest_nodes or []
    fig = go.Figure()

    # 1. Background Walkable Campus Paths (Clean Slate Gray)
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

    # 2. Highlighted Route Segments Connecting START to DESTINATION (Vibrant Emerald)
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

    # 3. Campus Location Nodes & Selective Dynamic Labels
    xs, ys, display_labels, colors, sizes, hovers = [], [], [], [], [], []
    for node_id, (x, y, category, floor, desc) in CAMPUS_COORDINATES.items():
        if node_id.startswith("JUNCTION_"):
            # Internal junction dots
            xs.append(x)
            ys.append(y)
            display_labels.append("")
            colors.append("#CBD5E1")
            sizes.append(5)
            hovers.append(f"Walkway Junction")
            continue

        xs.append(x)
        ys.append(y)
        clean_name = node_id.replace("_", " ")
        hovers.append(f"<b>{clean_name}</b><br>🏷️ Category: {category}<br>🏢 Floor: {floor}<br>📝 {desc}")

        # Label & Color selection
        if node_id == start_node:
            colors.append("#2563EB")  # Royal Blue for Start
            sizes.append(22)
            display_labels.append(f"📍 START: {clean_name}")
        elif node_id == dest_node:
            colors.append("#DC2626")  # Crimson Red for Destination
            sizes.append(22)
            display_labels.append(f"🎯 DEST: {clean_name}")
        elif node_id in active_route:
            colors.append("#10B981")  # Emerald for Active Path
            sizes.append(15)
            step_idx = active_route.index(node_id) + 1
            display_labels.append(f"#{step_idx} {clean_name}")
        elif node_id in nearest_nodes and not active_route:
            colors.append("#0284C7")  # Cyan for Nearest Places around starting location
            sizes.append(14)
            display_labels.append(f"⭐ {clean_name}")
        elif node_id in PRIMARY_LANDMARKS:
            colors.append("#475569")  # Dark Slate for Primary Landmarks
            sizes.append(11)
            display_labels.append(clean_name)
        else:
            colors.append("#94A3B8")  # Subtle Slate for regular locations
            sizes.append(8)
            display_labels.append("")  # Blank label prevents visual clumping

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
                       "• **Verified Turn-by-Turn Routes:** Pick or say your start and destination to connect them on the live map.\n"
                       "• **Photo Recognition & Nearest Places:** Upload any campus photo or pick an official preset; I will identify the building, list the nearest facilities, and let you navigate or ask follow-ups.\n"
                       "• **Campus Q&A:** Ask about departments, floors, food stalls, or request illustrative scenes.",
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

if "nearest_cache" not in st.session_state:
    st.session_state.nearest_cache = []

assistant = st.session_state.assistant

# -----------------------------------------------------------------------------
# SIDEBAR: QUICK ROUTE PLANNER, DIRECTORY & GEMINI KEY
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧭 Quick Route Planner")
    st.caption("Select origin and destination to connect them on the map:")

    # Selectable real locations (excluding pure junctions)
    navigable_keys = [k for k in sorted(list(CAMPUS_COORDINATES.keys())) if not k.startswith("JUNCTION_")]
    start_default_idx = navigable_keys.index("FOUNTAIN") if "FOUNTAIN" in navigable_keys else 0
    dest_default_idx = navigable_keys.index("SCHOOL_OF_LAW") if "SCHOOL_OF_LAW" in navigable_keys else 1

    sb_start = st.selectbox("📍 Starting Point", options=navigable_keys, index=start_default_idx, format_func=lambda x: x.replace("_", " "))
    sb_dest = st.selectbox("🎯 Destination", options=navigable_keys, index=dest_default_idx, format_func=lambda x: x.replace("_", " "))

    if st.button("🚀 Connect & Calculate Route", type="primary", use_container_width=True):
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
        st.session_state.nearest_cache = []
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
    <div class="hero-sub">Unified Campus Navigation • Photo Recognition & Nearest Location Discovery • Verified Landmark Paths</div>
    <div>
        <span class="badge-nav">🚶 Single Unified Map</span>
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
    st.caption("💡 Quick actions to try:")
    qp_cols = st.columns(3)
    with qp_cols[0]:
        if st.button("Floor of Design?", use_container_width=True):
            st.session_state.active_query = "Which floor is the School of Design on?"
    with qp_cols[1]:
        if st.button("Fountain ➔ Law", use_container_width=True):
            st.session_state.active_query = "From the fountain, guide me to the School of Law using landmarks."
    with qp_cols[2]:
        if st.button("What is near me?", use_container_width=True):
            st.session_state.active_query = "What locations and facilities are nearest to my current position?"

    # Chat Messages Scroll Area
    chat_container = st.container(height=430)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                if msg.get("uploaded_image") and os.path.exists(msg["uploaded_image"]):
                    st.image(msg["uploaded_image"], caption=f"📷 {os.path.basename(msg['uploaded_image'])}", width=250)
                st.markdown(msg["content"])
                if msg.get("citations"):
                    st.markdown(" ".join([f"<span class='citation-pill'>{c}</span>" for c in msg["citations"]]), unsafe_allow_html=True)
                if msg.get("generated_image") and os.path.exists(msg["generated_image"]):
                    st.image(msg["generated_image"], caption="🎨 Illustrative Visual Aid", use_container_width=True)

    # ACTIVE IMAGE FOCUS BANNER
    if st.session_state.active_image and os.path.exists(st.session_state.active_image):
        with st.container():
            st.markdown("""
            <div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 8px 12px; margin-bottom: 8px;">
                <span style="font-weight: 700; color: #1D4ED8;">🖼️ Active Photo in Focus:</span>
                <span style="color: #1E293B; font-weight: 500;">Ask follow-ups about signs, doors, nearest locations, or navigate from here!</span>
            </div>
            """, unsafe_allow_html=True)
            col_act1, col_act2, col_act3 = st.columns([2, 5, 3])
            with col_act1:
                st.image(st.session_state.active_image, width=70)
            with col_act2:
                st.markdown(f"**Photo:** `{os.path.basename(st.session_state.active_image)}`")
                if assistant.session_source:
                    loc_label = assistant.nav_graph.graph.nodes.get(assistant.session_source, {}).get("name", assistant.session_source)
                    st.caption(f"📍 Set as START: **{loc_label}**")
            with col_act3:
                if st.button("❌ Clear Photo", use_container_width=True):
                    st.session_state.active_image = None
                    st.session_state.nearest_cache = []
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
        "🎬 School of Media Studies (TV Studio)": "data/sample_images/media_studies.jpg",
        "💪 Campus Fitness Gym": "data/sample_images/gym.jpg",
        "🏧 24/7 Campus ATM": "data/sample_images/campus_atm.jpg"
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

        if resp.get("source_location"):
            assistant.session_source = resp["source_location"]
        if resp.get("nearest_locations"):
            st.session_state.nearest_cache = resp["nearest_locations"]
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

# ==================== RIGHT COLUMN: SINGLE UNIFIED MAP & NEAREST LOCATIONS ====================
with col_output:
    st.markdown("#### 🗺️ Unified Campus Map & Location Navigator")

    # Determine Active Route, Start & Destination on the Single Unified Map
    active_route_nodes = []
    start_point = assistant.session_source
    dest_point = None

    if st.session_state.last_route and st.session_state.last_route.get("success"):
        active_route_nodes = st.session_state.last_route.get("route", [])
        start_point = st.session_state.last_route.get("source")
        dest_point = st.session_state.last_route.get("destination")

    # Cache of nearest nodes around start_point
    nearest_node_ids = []
    if start_point:
        if not st.session_state.nearest_cache:
            st.session_state.nearest_cache = assistant.nav_graph.get_nearest_locations(start_point, count=5)
        nearest_node_ids = [item["node_id"] for item in st.session_state.nearest_cache]

    # Render Single Unified Interactive Plotly Map
    plotly_fig = make_interactive_campus_map(
        assistant.nav_graph.graph,
        active_route=active_route_nodes,
        start_node=start_point,
        dest_node=dest_point,
        nearest_nodes=nearest_node_ids
    )
    st.plotly_chart(plotly_fig, use_container_width=True, config={"displayModeBar": False})

    # ACTION CARD 1: Route Connected Steps (When START and DESTINATION are connected)
    if st.session_state.last_route and st.session_state.last_route.get("success"):
        r_data = st.session_state.last_route
        with st.container():
            st.markdown(f"##### 🚶 Connected Route ({len(r_data.get('steps', []))} verified path segments)")
            for s in r_data.get("steps", []):
                landmark_info = f" • *Landmark: {s['landmark']}*" if s.get('landmark') else ""
                vertical_info = " 🛗 [Elevator/Stairs]" if s.get('is_vertical') else ""
                st.markdown(f"<div class='step-box'><b>Step {s['step_number']}:</b> {s['instruction']}{landmark_info}{vertical_info}</div>", unsafe_allow_html=True)

    # ACTION CARD 2: Nearest Locations from Photo / Starting Position (Instant 1-Click Navigation)
    elif start_point:
        current_loc_name = assistant.nav_graph.graph.nodes.get(start_point, {}).get("name", start_point)
        with st.container():
            st.markdown(f"##### 🧭 Nearest Locations from **{current_loc_name}**")
            st.caption("Click 'Route ➔' to connect your current position to any nearby facility on the map:")
            
            nearest_list = st.session_state.nearest_cache or assistant.nav_graph.get_nearest_locations(start_point, count=4)
            for item in nearest_list[:4]:
                col_n1, col_n2 = st.columns([7, 3])
                with col_n1:
                    floor_txt = f" ({item['floor']})" if item['floor'] != "Ground" else ""
                    st.markdown(f"**{item['name']}**{floor_txt} • *{item['type'].capitalize()}*")
                with col_n2:
                    if st.button("Route ➔", key=f"btn_near_{item['node_id']}", help=f"Connect on map"):
                        route_calc = assistant.nav_graph.get_route(start_point, item["node_id"])
                        st.session_state.last_route = route_calc
                        st.session_state.messages.append({
                            "role": "user",
                            "content": f"Guide me to {item['name']} from {current_loc_name}"
                        })
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": assistant.nav_graph.generate_natural_directions(route_calc),
                            "citations": ["[campus_directions.pdf]"],
                            "route_result": route_calc,
                            "generated_image": None
                        })
                        st.rerun()

    # ACTION CARD 3: Default Campus Directory Overview
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
                - **Central Library:** Reading Halls & Archive
                """)
            with col_f2:
                st.markdown("""
                - **L Block (Ground):** Media Studies / TV Studio
                - **L Block (Floor 1):** Dean's Office
                - **Food Arcade:** Subway, Hatti Kaapi, Taj Delight
                - **Sports Complex:** Indoor Games & Gym
                - **Dining:** Domino's, Cafe Feasto, Lassi House
                """)
