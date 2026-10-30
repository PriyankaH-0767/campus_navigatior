"""
Campus Navigation Graph Module
Deterministic, verified pedestrian graph for CampusDrive AI.
Uses NetworkX to provide verified shortest-path routing, landmark-anchored instructions,
nearest-location spatial queries, and strict rejection of unmapped routes to prevent hallucination.
"""

from typing import Dict, List, Optional, Tuple, Any
import networkx as nx
import json
import os

class CampusNavigationGraph:
    def __init__(self, registry_path: Optional[str] = None):
        self.graph = nx.Graph()
        self.node_metadata: Dict[str, Dict[str, Any]] = {}
        self.registry_path = registry_path
        self._build_verified_graph()

    def _build_verified_graph(self):
        """Constructs the comprehensive campus graph integrating all 64 places and verified walkways."""
        # 1. Register canonical places, landmarks, facilities, and academic wings
        verified_nodes = [
            ("UNIVERSITY_ENTRANCE", {"name": "University Entrance", "type": "entrance", "floor": "Ground"}),
            ("FOUNTAIN", {"name": "Campus Fountain", "type": "landmark", "floor": "Ground"}),
            ("JUNCTION_FOUNTAIN_RIGHT", {"name": "Avenue Junction", "type": "junction", "floor": "Ground"}),
            ("JUNCTION_FIRST_LEFT", {"name": "First Left Junction", "type": "junction", "floor": "Ground"}),
            ("UDAYA_UPAHARA", {"name": "Udaya Upahar", "type": "food", "floor": "Ground"}),
            ("JUNCTION_SECOND_LEFT", {"name": "Second Left Junction", "type": "junction", "floor": "Ground"}),
            ("ENGINEERING_BLOCK", {"name": "Engineering Block", "type": "academic", "floor": "Ground"}),
            ("CIVIL_DEPARTMENT", {"name": "Department of Civil Engineering", "type": "academic", "floor": "Ground"}),
            ("COMPUTER_LAB", {"name": "Computer Lab", "type": "facility", "floor": "Ground"}),
            ("FULL_STACK_LAB", {"name": "Full Stack Development Lab", "type": "academic", "floor": "Ground"}),
            ("AI_CENTRE_OF_EXCELLENCE", {"name": "AI Centre of Excellence", "type": "research", "floor": "Ground"}),
            ("VR_STUDIO", {"name": "VR Studio", "type": "research", "floor": "Ground"}),
            ("ADMISSION_BLOCK", {"name": "Admission Block (Admin)", "type": "admin", "floor": "Ground"}),
            ("REGISTRAR_OFFICE", {"name": "Office of the Registrar", "type": "office", "floor": "1st Floor"}),
            ("CONTROLLER_EXAMINATION", {"name": "Office of Controller of Examination", "type": "office", "floor": "Ground"}),
            ("DEAN_OFFICE_MBA", {"name": "Dean Office of MBA Department", "type": "office", "floor": "1st Floor"}),
            ("FEE_DEPARTMENT", {"name": "Fee Department", "type": "office", "floor": "Ground"}),
            ("OFFICE_INTERNATIONAL_AFFAIRS", {"name": "Office of International Affairs", "type": "office", "floor": "Ground"}),
            ("CAMPUS_ATM", {"name": "24/7 ATM", "type": "service", "floor": "Ground"}),
            ("FOOD_STALLS_ADMISSION", {"name": "Food Stalls (Subway, Hatti Kaapi, Aromas, Taj)", "type": "food", "floor": "Ground"}),
            ("CAFE_FEASTO", {"name": "Cafe Feasto", "type": "food", "floor": "Ground"}),
            ("HATTI_KAAPI", {"name": "Hatti Kaapi", "type": "food", "floor": "Ground"}),
            ("JUNCTION_SPORTS_PATH", {"name": "Sports Path Turnoff", "type": "junction", "floor": "Ground"}),
            ("SPORTS_AREA", {"name": "Sports Area & Outdoor Courts", "type": "sports", "floor": "Ground"}),
            ("INDOOR_GAMES", {"name": "Indoor Games Hall", "type": "sports", "floor": "Ground"}),
            ("GYM", {"name": "Campus Fitness Gym", "type": "sports", "floor": "Ground"}),
            ("DOMINOS", {"name": "Domino's Pizza", "type": "food", "floor": "Ground"}),
            ("CENTRAL_LIBRARY", {"name": "Central Campus Library", "type": "facility", "floor": "Ground & 1st"}),
            ("CAFETERIA", {"name": "Central Cafeteria", "type": "food", "floor": "Ground"}),
            ("AMPHITHEATER", {"name": "Amphitheater", "type": "landmark", "floor": "Ground"}),
            ("AUDITORIUM", {"name": "Main Auditorium", "type": "facility", "floor": "Ground"}),
            ("DSA_OFFICE", {"name": "DSA Office", "type": "office", "floor": "Ground"}),
            ("MUSICAL_ROOM", {"name": "Musical Room", "type": "facility", "floor": "Ground"}),
            ("MEDICAL_ROOM", {"name": "Medical Room (Manipal Clinics)", "type": "service", "floor": "Ground"}),
            ("TRANSPORT_DEPARTMENT", {"name": "Transport Department", "type": "office", "floor": "Ground"}),
            ("M_BLOCK", {"name": "M Block", "type": "academic", "floor": "Ground"}),
            ("JUNCTION_STATIONERY", {"name": "Stationery Junction", "type": "junction", "floor": "Ground"}),
            ("STATIONERY", {"name": "Stationery & Photocopy Shop", "type": "service", "floor": "Ground"}),
            ("D_BLOCK", {"name": "D Block Entrance", "type": "academic", "floor": "Ground"}),
            ("SCHOOL_OF_DESIGN", {"name": "School of Design", "type": "academic", "floor": "5th Floor"}),
            ("JUNCTION_D_LEFT", {"name": "D Block West Junction", "type": "junction", "floor": "Ground"}),
            ("E_BLOCK", {"name": "E Block", "type": "academic", "floor": "Ground"}),
            ("RD_CENTRE", {"name": "Research and Development Centre", "type": "research", "floor": "Ground & 1st"}),
            ("F_BLOCK", {"name": "F Block", "type": "academic", "floor": "Ground"}),
            ("L_BLOCK", {"name": "L Block", "type": "academic", "floor": "Ground"}),
            ("NEXUS_CORE", {"name": "Nexus Core Transition", "type": "junction", "floor": "Ground"}),
            ("SCHOOL_OF_MEDIA_STUDIES", {"name": "School of Media Studies (TV Studio)", "type": "academic", "floor": "Ground"}),
            ("DEAN_OFFICE_L_BLOCK", {"name": "Dean's Office (L Block)", "type": "office", "floor": "1st Floor"}),
            ("DEAN_OFFICE_PSCS", {"name": "Dean Office PSCS", "type": "office", "floor": "1st Floor"}),
            ("FOOD_STALLS_L_BLOCK", {"name": "Food Arcade (V Mart, Crazy Cups, Lassi House)", "type": "food", "floor": "Ground"}),
            ("VJ_MART", {"name": "VJ Mart", "type": "food", "floor": "Ground"}),
            ("CRAZY_CUPS", {"name": "Crazy Cups", "type": "food", "floor": "Ground"}),
            ("LASSI_HOUSE", {"name": "Lassi House", "type": "food", "floor": "Ground"}),
            ("H_BLOCK", {"name": "H Block", "type": "academic", "floor": "Ground"}),
            ("J_BLOCK", {"name": "J Block", "type": "academic", "floor": "Ground"}),
            ("K_BLOCK", {"name": "K Block", "type": "academic", "floor": "Ground"}),
            ("N_BLOCK", {"name": "N Block", "type": "academic", "floor": "Ground"}),
            ("P_BLOCK", {"name": "P Block", "type": "academic", "floor": "Ground"}),
            ("Q_BLOCK", {"name": "Q Block", "type": "academic", "floor": "Ground"}),
            ("R_BLOCK", {"name": "R Block", "type": "academic", "floor": "Ground"}),
            ("S_BLOCK", {"name": "S Block", "type": "academic", "floor": "Ground"}),
            ("SCHOOL_OF_LAW", {"name": "School of Law", "type": "academic", "floor": "5th Floor"}),
            ("LAW_LIBRARY", {"name": "Law Library", "type": "facility", "floor": "5th Floor"}),
            ("U_BLOCK", {"name": "U Block", "type": "academic", "floor": "Ground"})
        ]

        for node_id, attrs in verified_nodes:
            self.graph.add_node(node_id, **attrs)
            self.node_metadata[node_id] = attrs

        # 2. Add verified pedestrian edges with distances, turn instructions, and landmarks
        verified_edges = [
            # Main Entrance to Fountain
            ("UNIVERSITY_ENTRANCE", "FOUNTAIN", {
                "distance_m": 40,
                "turn_instruction": "From University Entrance, walk straight along the palm tree avenue to the central Campus Fountain.",
                "landmark": "Main Entrance Palm Driveway",
                "verified": True
            }),
            # Fountain to right avenue
            ("FOUNTAIN", "JUNCTION_FOUNTAIN_RIGHT", {
                "distance_m": 15,
                "turn_instruction": "From Fountain, take a right onto the main campus avenue.",
                "landmark": "Campus Fountain",
                "verified": True
            }),
            ("JUNCTION_FOUNTAIN_RIGHT", "JUNCTION_FIRST_LEFT", {
                "distance_m": 25,
                "turn_instruction": "Walk straight along the avenue to the first left opening.",
                "landmark": "Landscaped palm walkway",
                "verified": True
            }),
            ("JUNCTION_FIRST_LEFT", "UDAYA_UPAHARA", {
                "distance_m": 20,
                "turn_instruction": "Take the first left turn towards Udaya Upahar dining area.",
                "landmark": "Udaya Upahar signage",
                "verified": True
            }),
            # Avenue to Engineering Block
            ("JUNCTION_FIRST_LEFT", "JUNCTION_SECOND_LEFT", {
                "distance_m": 35,
                "turn_instruction": "Continue straight along the avenue to the second left turn.",
                "landmark": "Campus central trees",
                "verified": True
            }),
            ("JUNCTION_SECOND_LEFT", "ENGINEERING_BLOCK", {
                "distance_m": 20,
                "turn_instruction": "Turn left at the second opening into the Engineering Block entrance.",
                "landmark": "Engineering Block portico",
                "verified": True
            }),
            ("ENGINEERING_BLOCK", "CIVIL_DEPARTMENT", {
                "distance_m": 15,
                "turn_instruction": "Inside Engineering Block, take the ground corridor to Department of Civil Engineering.",
                "landmark": "Civil Engineering wing plaque",
                "verified": True
            }),
            ("ENGINEERING_BLOCK", "COMPUTER_LAB", {
                "distance_m": 20,
                "turn_instruction": "Proceed along the engineering concourse to the Central Computer Lab.",
                "landmark": "Computer Lab glass doors",
                "verified": True
            }),
            ("ENGINEERING_BLOCK", "FULL_STACK_LAB", {
                "distance_m": 25,
                "turn_instruction": "Head towards the computing labs corridor to enter the Full Stack Development Lab.",
                "landmark": "Full Stack Lab entrance",
                "verified": True
            }),
            ("ENGINEERING_BLOCK", "AI_CENTRE_OF_EXCELLENCE", {
                "distance_m": 30,
                "turn_instruction": "Walk to the advanced technology wing to reach the AI Centre of Excellence.",
                "landmark": "NVIDIA AI Centre of Excellence plaque",
                "verified": True
            }),
            ("ENGINEERING_BLOCK", "VR_STUDIO", {
                "distance_m": 30,
                "turn_instruction": "Walk past the AI centre to reach the VR Studio.",
                "landmark": "VR Studio sign",
                "verified": True
            }),
            # Admission / Admin Complex
            ("ENGINEERING_BLOCK", "ADMISSION_BLOCK", {
                "distance_m": 15,
                "turn_instruction": "Walk right beside the Engineering Block to reach the Admission Block.",
                "landmark": "Admission Block entrance atrium",
                "verified": True
            }),
            ("ADMISSION_BLOCK", "REGISTRAR_OFFICE", {
                "distance_m": 10,
                "turn_instruction": "Inside Admission Block, take the stairs or elevator to the 1st floor for the Office of the Registrar.",
                "landmark": "Registrar Office sign (Counter-01, 02, 03)",
                "is_vertical": True,
                "verified": True
            }),
            ("ADMISSION_BLOCK", "CONTROLLER_EXAMINATION", {
                "distance_m": 10,
                "turn_instruction": "Walk past the reception of Admission Block to the Controller of Examination counters.",
                "landmark": "Exam branch counter sign",
                "verified": True
            }),
            ("ADMISSION_BLOCK", "DEAN_OFFICE_MBA", {
                "distance_m": 15,
                "turn_instruction": "Inside Admin Block, take the stairs to the 1st floor to reach the Dean Office of MBA Department.",
                "landmark": "Dean Office MBA signage",
                "is_vertical": True,
                "verified": True
            }),
            ("ADMISSION_BLOCK", "FEE_DEPARTMENT", {
                "distance_m": 10,
                "turn_instruction": "On the ground floor of Admin Block, head to the Fee Department counters.",
                "landmark": "Fee Department counter glass",
                "verified": True
            }),
            ("ADMISSION_BLOCK", "OFFICE_INTERNATIONAL_AFFAIRS", {
                "distance_m": 12,
                "turn_instruction": "Walk to the dedicated lounge on the ground floor for Office of International Affairs.",
                "landmark": "Office of International Affairs blue board",
                "verified": True
            }),
            ("ADMISSION_BLOCK", "CAMPUS_ATM", {
                "distance_m": 15,
                "turn_instruction": "Step outside Admission Block along the sidewalk to the 24/7 ATM kiosk.",
                "landmark": "Campus 24-Hour ATM",
                "verified": True
            }),
            ("ADMISSION_BLOCK", "FOOD_STALLS_ADMISSION", {
                "distance_m": 20,
                "turn_instruction": "Cross directly opposite the Admission Block to the food stalls arcade.",
                "landmark": "Subway & Hatti Kaapi stalls",
                "verified": True
            }),
            ("FOOD_STALLS_ADMISSION", "CAFE_FEASTO", {
                "distance_m": 10,
                "turn_instruction": "Inside the food stalls arcade, walk to Cafe Feasto.",
                "landmark": "Cafe Feasto counter",
                "verified": True
            }),
            ("FOOD_STALLS_ADMISSION", "HATTI_KAAPI", {
                "distance_m": 10,
                "turn_instruction": "Inside the food stalls arcade, walk to Hatti Kaapi.",
                "landmark": "Hatti Kaapi kiosk",
                "verified": True
            }),
            ("JUNCTION_SECOND_LEFT", "FOOD_STALLS_ADMISSION", {
                "distance_m": 25,
                "turn_instruction": "Continue straight; on your right side you will see the food stalls opposite Admission Block.",
                "landmark": "Food court signboards",
                "verified": True
            }),
            # Sports Complex & Domino's
            ("FOOD_STALLS_ADMISSION", "JUNCTION_SPORTS_PATH", {
                "distance_m": 30,
                "turn_instruction": "Walk into the food stalls corridor and follow the path extending toward the right.",
                "landmark": "Outdoor food seating",
                "verified": True
            }),
            ("JUNCTION_SPORTS_PATH", "SPORTS_AREA", {
                "distance_m": 40,
                "turn_instruction": "Follow the path on the right into the open athletic sports courts.",
                "landmark": "Sports courts fencing",
                "verified": True
            }),
            ("SPORTS_AREA", "INDOOR_GAMES", {
                "distance_m": 15,
                "turn_instruction": "Enter the sports building to reach the tournament Indoor Games Hall.",
                "landmark": "Indoor table tennis hall",
                "verified": True
            }),
            ("SPORTS_AREA", "GYM", {
                "distance_m": 20,
                "turn_instruction": "Walk to the fitness pavilion inside the sports building to reach the Campus Gym.",
                "landmark": "Campus Gym equipment",
                "verified": True
            }),
            ("JUNCTION_SPORTS_PATH", "DOMINOS", {
                "distance_m": 25,
                "turn_instruction": "Walk past the food pavilion towards the Domino's pizza outlet kiosk.",
                "landmark": "Domino's red and blue logo",
                "verified": True
            }),
            # Facilities & West Concourse
            ("ADMISSION_BLOCK", "AMPHITHEATER", {
                "distance_m": 45,
                "turn_instruction": "Walk through the landscaped central terrace to the open-air Amphitheater.",
                "landmark": "Green tiered steps",
                "verified": True
            }),
            ("AMPHITHEATER", "AUDITORIUM", {
                "distance_m": 30,
                "turn_instruction": "Walk past the amphitheater gardens to the grand steps of the Auditorium.",
                "landmark": "Auditorium marble steps",
                "verified": True
            }),
            ("AMPHITHEATER", "CAFETERIA", {
                "distance_m": 35,
                "turn_instruction": "Walk past the open lawn into the Central Student Cafeteria.",
                "landmark": "Central Cafeteria entrance",
                "verified": True
            }),
            ("ADMISSION_BLOCK", "CENTRAL_LIBRARY", {
                "distance_m": 40,
                "turn_instruction": "Walk past the central garden walkway to enter the Central Campus Library.",
                "landmark": "Central Library entrance turnstiles",
                "verified": True
            }),
            ("CENTRAL_LIBRARY", "MEDICAL_ROOM", {
                "distance_m": 20,
                "turn_instruction": "Next to the library entrance, step into the Campus Medical Room (Manipal Clinics).",
                "landmark": "Manipal Clinics Medical Room",
                "verified": True
            }),
            ("CENTRAL_LIBRARY", "DSA_OFFICE", {
                "distance_m": 25,
                "turn_instruction": "Walk along the shaded veranda to reach the DSA Office.",
                "landmark": "DSA Office entrance",
                "verified": True
            }),
            ("DSA_OFFICE", "MUSICAL_ROOM", {
                "distance_m": 20,
                "turn_instruction": "Walk beside the DSA courtyard to reach the Musical Room canopy.",
                "landmark": "Musical Room open canopy",
                "verified": True
            }),
            ("ADMISSION_BLOCK", "TRANSPORT_DEPARTMENT", {
                "distance_m": 30,
                "turn_instruction": "Walk down the side concourse to the Transport Department.",
                "landmark": "Transport Department office",
                "verified": True
            }),
            ("TRANSPORT_DEPARTMENT", "M_BLOCK", {
                "distance_m": 25,
                "turn_instruction": "Walk past the transport office to reach M Block classrooms.",
                "landmark": "M Block directional sign",
                "verified": True
            }),
            # D, E, F, L Academic Wings
            ("ADMISSION_BLOCK", "JUNCTION_STATIONERY", {
                "distance_m": 35,
                "turn_instruction": "Head straight ahead past Admission Block toward the Stationery shop.",
                "landmark": "Stationery shop building",
                "verified": True
            }),
            ("JUNCTION_STATIONERY", "STATIONERY", {
                "distance_m": 10,
                "turn_instruction": "Turn slightly right to enter the campus Stationery and photocopy shop.",
                "landmark": "Stationery storefront",
                "verified": True
            }),
            ("JUNCTION_STATIONERY", "D_BLOCK", {
                "distance_m": 15,
                "turn_instruction": "Continue straight past the stationery shop into D Block main entrance.",
                "landmark": "D Block Entrance foyer",
                "verified": True
            }),
            ("D_BLOCK", "SCHOOL_OF_DESIGN", {
                "distance_m": 15,
                "turn_instruction": "Inside D Block, take the stairs or elevator to the 5th floor. The School of Design is located on the entire fifth floor.",
                "landmark": "Blue SCHOOL OF DESIGN overhead signage",
                "is_vertical": True,
                "verified": True
            }),
            ("D_BLOCK", "JUNCTION_D_LEFT", {
                "distance_m": 20,
                "turn_instruction": "Take the left corridor exiting from D Block.",
                "landmark": "D Block west connector",
                "verified": True
            }),
            ("JUNCTION_D_LEFT", "E_BLOCK", {
                "distance_m": 30,
                "turn_instruction": "Walk ahead along the covered wing to reach E Block.",
                "landmark": "E Block Seminar Hall",
                "verified": True
            }),
            ("E_BLOCK", "RD_CENTRE", {
                "distance_m": 10,
                "turn_instruction": "Enter E Block; the Research and Development (R&D) Centre is situated on the ground and first floors.",
                "landmark": "R&D Centre and AI lab plaque",
                "is_vertical": True,
                "verified": True
            }),
            ("E_BLOCK", "F_BLOCK", {
                "distance_m": 25,
                "turn_instruction": "Proceed past E Block seminar hall to F Block.",
                "landmark": "F Block Seminar Hall",
                "verified": True
            }),
            ("F_BLOCK", "NEXUS_CORE", {
                "distance_m": 20,
                "turn_instruction": "Pass through the Nexus Core transition underpass towards L Block.",
                "landmark": "NEXUS CORE overhead signage",
                "verified": True
            }),
            ("NEXUS_CORE", "L_BLOCK", {
                "distance_m": 20,
                "turn_instruction": "Exit the Nexus Core passageway into the L Block entrance concourse.",
                "landmark": "L Block entrance concourse",
                "verified": True
            }),
            ("L_BLOCK", "SCHOOL_OF_MEDIA_STUDIES", {
                "distance_m": 10,
                "turn_instruction": "On the ground floor of L Block, enter the School of Media Studies and TV Studio.",
                "landmark": "MEDIA STUDIES / TV STUDIO entrance",
                "verified": True
            }),
            ("L_BLOCK", "DEAN_OFFICE_L_BLOCK", {
                "distance_m": 10,
                "turn_instruction": "Take the stairs to the first floor of L Block to reach the Dean's Office.",
                "landmark": "Dean Office notice board",
                "is_vertical": True,
                "verified": True
            }),
            ("L_BLOCK", "DEAN_OFFICE_PSCS", {
                "distance_m": 12,
                "turn_instruction": "On the first floor of L Block, walk down the corridor to Dean Office PSCS.",
                "landmark": "Dean Office PSCS plaque",
                "is_vertical": True,
                "verified": True
            }),
            ("L_BLOCK", "FOOD_STALLS_L_BLOCK", {
                "distance_m": 20,
                "turn_instruction": "Step out to the food stalls arcade featuring VJ Mart, Crazy Cups, and Lassi House.",
                "landmark": "Food stalls arcade sign",
                "verified": True
            }),
            ("FOOD_STALLS_L_BLOCK", "VJ_MART", {
                "distance_m": 10,
                "turn_instruction": "Inside the food arcade, walk to VJ Mart kiosk.",
                "landmark": "VJ Mart kiosk",
                "verified": True
            }),
            ("FOOD_STALLS_L_BLOCK", "CRAZY_CUPS", {
                "distance_m": 10,
                "turn_instruction": "Inside the food arcade, walk to Crazy Cups stall.",
                "landmark": "Crazy Cups kiosk",
                "verified": True
            }),
            ("FOOD_STALLS_L_BLOCK", "LASSI_HOUSE", {
                "distance_m": 10,
                "turn_instruction": "Inside the food arcade, walk to Lassi House.",
                "landmark": "Lassi House signage",
                "verified": True
            }),
            # Engineering Spine: H, J, K -> N, P, Q, R, S, U
            ("ENGINEERING_BLOCK", "H_BLOCK", {
                "distance_m": 20,
                "turn_instruction": "Enter Engineering Block and take the internal concourse towards H Block.",
                "landmark": "H Block corridor",
                "verified": True
            }),
            ("H_BLOCK", "J_BLOCK", {
                "distance_m": 20,
                "turn_instruction": "Walk straight through the internal corridor from H Block to J Block.",
                "landmark": "J Block wing",
                "verified": True
            }),
            ("J_BLOCK", "K_BLOCK", {
                "distance_m": 20,
                "turn_instruction": "Continue along the enclosed corridor from J Block to K Block.",
                "landmark": "K Block wing",
                "verified": True
            }),
            ("K_BLOCK", "N_BLOCK", {
                "distance_m": 25,
                "turn_instruction": "Exit the K Block corridor into the N Block connector walkway.",
                "landmark": "N Block entrance arch",
                "verified": True
            }),
            ("N_BLOCK", "P_BLOCK", {
                "distance_m": 35,
                "turn_instruction": "Follow the main pedestrian walkway from N Block to P Block.",
                "landmark": "P Block academic sign",
                "verified": True
            }),
            ("P_BLOCK", "FOOD_STALLS_L_BLOCK", {
                "distance_m": 15,
                "turn_instruction": "On the right side of P Block, you can access the food stalls arcade.",
                "landmark": "P Block food pavilion",
                "verified": True
            }),
            ("P_BLOCK", "Q_BLOCK", {
                "distance_m": 30,
                "turn_instruction": "Proceed south past P Block to Q Block.",
                "landmark": "Q Block corridor",
                "verified": True
            }),
            ("Q_BLOCK", "R_BLOCK", {
                "distance_m": 30,
                "turn_instruction": "Continue along the covered passage from Q Block to R Block.",
                "landmark": "R Block sign",
                "verified": True
            }),
            ("R_BLOCK", "S_BLOCK", {
                "distance_m": 35,
                "turn_instruction": "Walk from R Block to reach S Block entrance.",
                "landmark": "S Block entrance lobby",
                "verified": True
            }),
            ("S_BLOCK", "SCHOOL_OF_LAW", {
                "distance_m": 15,
                "turn_instruction": "Inside S Block, take the elevator or staircase to the 5th floor for the School of Law.",
                "landmark": "School of Law plaque",
                "is_vertical": True,
                "verified": True
            }),
            ("SCHOOL_OF_LAW", "LAW_LIBRARY", {
                "distance_m": 10,
                "turn_instruction": "On the 5th floor of S Block, enter the dedicated Law Library.",
                "landmark": "Law Library entrance door",
                "verified": True
            }),
            ("S_BLOCK", "U_BLOCK", {
                "distance_m": 25,
                "turn_instruction": "Walk past S Block to reach U Block at the end of the academic complex.",
                "landmark": "U Block terminal",
                "verified": True
            })
        ]

        for u, v, attrs in verified_edges:
            self.graph.add_edge(u, v, **attrs)

    def resolve_location_id(self, query: str) -> Optional[str]:
        """Maps user queries or aliases to canonical node IDs."""
        q = query.strip().upper().replace(" ", "_").replace("-", "_")
        if q in self.graph:
            return q
            
        clean_q = query.strip().lower()
        
        # Comprehensive alias dictionary covering all campus locations
        alias_map = {
            "entrance": "UNIVERSITY_ENTRANCE",
            "main gate": "UNIVERSITY_ENTRANCE",
            "gate": "UNIVERSITY_ENTRANCE",
            "university entrance": "UNIVERSITY_ENTRANCE",
            "fountain": "FOUNTAIN",
            "campus fountain": "FOUNTAIN",
            "central fountain": "FOUNTAIN",
            "udaya": "UDAYA_UPAHARA",
            "udaya upahara": "UDAYA_UPAHARA",
            "udaya upahar": "UDAYA_UPAHARA",
            "engineering block": "ENGINEERING_BLOCK",
            "engg block": "ENGINEERING_BLOCK",
            "civil": "CIVIL_DEPARTMENT",
            "civil engineering": "CIVIL_DEPARTMENT",
            "department of civil": "CIVIL_DEPARTMENT",
            "computer lab": "COMPUTER_LAB",
            "full stack": "FULL_STACK_LAB",
            "full stack lab": "FULL_STACK_LAB",
            "ai centre": "AI_CENTRE_OF_EXCELLENCE",
            "ai center": "AI_CENTRE_OF_EXCELLENCE",
            "ai centre of excellence": "AI_CENTRE_OF_EXCELLENCE",
            "vr studio": "VR_STUDIO",
            "admission block": "ADMISSION_BLOCK",
            "admin block": "ADMISSION_BLOCK",
            "admissions": "ADMISSION_BLOCK",
            "registrar": "REGISTRAR_OFFICE",
            "registrar's office": "REGISTRAR_OFFICE",
            "office of the registrar": "REGISTRAR_OFFICE",
            "office of registrar": "REGISTRAR_OFFICE",
            "controller examination": "CONTROLLER_EXAMINATION",
            "office of controller examination": "CONTROLLER_EXAMINATION",
            "dean office mba": "DEAN_OFFICE_MBA",
            "mba": "DEAN_OFFICE_MBA",
            "fee department": "FEE_DEPARTMENT",
            "fee counter": "FEE_DEPARTMENT",
            "fees": "FEE_DEPARTMENT",
            "international affairs": "OFFICE_INTERNATIONAL_AFFAIRS",
            "office of international affairs": "OFFICE_INTERNATIONAL_AFFAIRS",
            "atm": "CAMPUS_ATM",
            "campus atm": "CAMPUS_ATM",
            "food stalls": "FOOD_STALLS_ADMISSION",
            "food court": "FOOD_STALLS_ADMISSION",
            "subway": "FOOD_STALLS_ADMISSION",
            "cafe feasto": "CAFE_FEASTO",
            "feasto": "CAFE_FEASTO",
            "hatti kaapi": "HATTI_KAAPI",
            "taj delight": "FOOD_STALLS_ADMISSION",
            "sports": "SPORTS_AREA",
            "sports area": "SPORTS_AREA",
            "sports complex": "SPORTS_AREA",
            "basketball": "SPORTS_AREA",
            "volleyball": "SPORTS_AREA",
            "indoor games": "INDOOR_GAMES",
            "table tennis": "INDOOR_GAMES",
            "gym": "GYM",
            "fitness gym": "GYM",
            "gymnasium": "GYM",
            "dominos": "DOMINOS",
            "domino's": "DOMINOS",
            "library": "CENTRAL_LIBRARY",
            "central library": "CENTRAL_LIBRARY",
            "cafeteria": "CAFETERIA",
            "canteen": "CAFETERIA",
            "amphitheater": "AMPHITHEATER",
            "auditorium": "AUDITORIUM",
            "dsa": "DSA_OFFICE",
            "dsa office": "DSA_OFFICE",
            "musical room": "MUSICAL_ROOM",
            "music room": "MUSICAL_ROOM",
            "medical room": "MEDICAL_ROOM",
            "clinic": "MEDICAL_ROOM",
            "manipal clinics": "MEDICAL_ROOM",
            "transport department": "TRANSPORT_DEPARTMENT",
            "transport office": "TRANSPORT_DEPARTMENT",
            "m block": "M_BLOCK",
            "block m": "M_BLOCK",
            "stationery": "STATIONERY",
            "stationary": "STATIONERY",
            "d block": "D_BLOCK",
            "block d": "D_BLOCK",
            "school of design": "SCHOOL_OF_DESIGN",
            "design school": "SCHOOL_OF_DESIGN",
            "e block": "E_BLOCK",
            "r&d centre": "RD_CENTRE",
            "r&d": "RD_CENTRE",
            "research and development": "RD_CENTRE",
            "f block": "F_BLOCK",
            "nexus core": "NEXUS_CORE",
            "l block": "L_BLOCK",
            "school of media studies": "SCHOOL_OF_MEDIA_STUDIES",
            "media studies": "SCHOOL_OF_MEDIA_STUDIES",
            "tv studio": "SCHOOL_OF_MEDIA_STUDIES",
            "dean office": "DEAN_OFFICE_L_BLOCK",
            "dean office pscs": "DEAN_OFFICE_PSCS",
            "pscs": "DEAN_OFFICE_PSCS",
            "v mart": "VJ_MART",
            "vj mart": "VJ_MART",
            "crazy cups": "CRAZY_CUPS",
            "lassi house": "LASSI_HOUSE",
            "lassi area": "LASSI_HOUSE",
            "n block": "N_BLOCK",
            "p block": "P_BLOCK",
            "q block": "Q_BLOCK",
            "r block": "R_BLOCK",
            "s block": "S_BLOCK",
            "school of law": "SCHOOL_OF_LAW",
            "law school": "SCHOOL_OF_LAW",
            "law library": "LAW_LIBRARY",
            "u block": "U_BLOCK"
        }
        
        if clean_q in alias_map:
            return alias_map[clean_q]
            
        for alias, node_id in alias_map.items():
            if alias in clean_q or clean_q in alias:
                return node_id
                
        return None

    def get_route(self, source_query: str, destination_query: str, weight: str = "distance_m") -> Dict[str, Any]:
        """
        Calculates verified route between source and destination.
        Returns detailed path, step instructions, landmarks, and validation status.
        Never hallucinates unmapped paths.
        """
        source_id = self.resolve_location_id(source_query)
        dest_id = self.resolve_location_id(destination_query)

        if not source_id:
            return {
                "success": False,
                "error": f"Starting point '{source_query}' is not mapped or recognized.",
                "clarification_needed": True,
                "route": [],
                "steps": [],
                "total_distance_m": 0
            }

        if not dest_id:
            return {
                "success": False,
                "error": f"Destination '{destination_query}' is not mapped or recognized. Please clarify.",
                "clarification_needed": True,
                "route": [],
                "steps": [],
                "total_distance_m": 0
            }

        if source_id == dest_id:
            dest_name = self.graph.nodes[dest_id].get("name", dest_id)
            floor_info = self.graph.nodes[dest_id].get("floor", "current level")
            return {
                "success": True,
                "error": None,
                "source": source_id,
                "destination": dest_id,
                "route": [source_id],
                "steps": [f"You are already at {dest_name} ({floor_info})."],
                "total_distance_m": 0,
                "is_same_location": True
            }

        try:
            path = nx.shortest_path(self.graph, source=source_id, target=dest_id, weight=weight)
            
            steps = []
            total_dist = 0
            landmarks_seen = []

            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                edge_data = self.graph.get_edge_data(u, v) or {}
                dist = edge_data.get("distance_m", 0)
                total_dist += dist
                instruction = edge_data.get("turn_instruction", f"Walk from {u} to {v}.")
                landmark = edge_data.get("landmark", "")
                if landmark and landmark not in landmarks_seen:
                    landmarks_seen.append(landmark)
                steps.append({
                    "step_number": i + 1,
                    "from_node": u,
                    "to_node": v,
                    "instruction": instruction,
                    "distance_m": dist,
                    "landmark": landmark,
                    "is_vertical": edge_data.get("is_vertical", False)
                })

            return {
                "success": True,
                "error": None,
                "source": source_id,
                "source_name": self.graph.nodes[source_id].get("name", source_id),
                "destination": dest_id,
                "destination_name": self.graph.nodes[dest_id].get("name", dest_id),
                "route": path,
                "steps": steps,
                "total_distance_m": total_dist,
                "landmarks": landmarks_seen,
                "is_verified": True
            }

        except nx.NetworkXNoPath:
            return {
                "success": False,
                "error": f"No verified traversable route found between {source_id} and {dest_id}.",
                "route": [],
                "steps": [],
                "total_distance_m": 0
            }

    def get_nearest_locations(self, location_query: str, count: int = 5) -> List[Dict[str, Any]]:
        """
        Calculates nearest real campus locations and facilities from a given location.
        Filters out internal junction waypoints to return actionable destinations.
        """
        loc_id = self.resolve_location_id(location_query)
        if not loc_id or loc_id not in self.graph:
            return []

        lengths = nx.single_source_dijkstra_path_length(self.graph, loc_id, weight="distance_m")
        sorted_nodes = sorted(lengths.items(), key=lambda x: x[1])

        results = []
        for target_node, dist in sorted_nodes:
            if target_node == loc_id or target_node.startswith("JUNCTION_"):
                continue
            attrs = self.graph.nodes.get(target_node, {})
            results.append({
                "node_id": target_node,
                "name": attrs.get("name", target_node.replace("_", " ")),
                "type": attrs.get("type", "facility"),
                "floor": attrs.get("floor", "Ground"),
                "distance_m": dist
            })
            if len(results) >= count:
                break

        return results

    def generate_natural_directions(self, route_result: Dict[str, Any]) -> str:
        """Converts graph route result into natural turn-by-turn guidance without raw distances."""
        if not route_result.get("success"):
            return route_result.get("error", "Route calculation failed.")

        if route_result.get("is_same_location"):
            return route_result["steps"][0]

        source_name = route_result["source_name"]
        dest_name = route_result["destination_name"]
        steps = route_result["steps"]

        lines = [
            f"🚶 **Verified Route from {source_name} to {dest_name}** ({len(steps)} verified path segments)",
            ""
        ]

        for s in steps:
            landmark_txt = f" [Landmark: *{s['landmark']}*]" if s['landmark'] else ""
            vertical_txt = " 🛗 [Vertical Floor Transit]" if s.get('is_vertical') else ""
            lines.append(f"{s['step_number']}. {s['instruction']}{landmark_txt}{vertical_txt}")

        lines.append("")
        lines.append("✅ *Directions verified against confirmed campus pathways.*")
        return "\n".join(lines)
