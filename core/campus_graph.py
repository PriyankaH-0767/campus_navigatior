"""
Campus Navigation Graph Module
Deterministic, verified pedestrian graph for Smart Campus Explorer AI.
Uses NetworkX to provide verified shortest-path routing, landmark-anchored instructions,
and strict rejection of unmapped routes to prevent hallucination.
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
        """Constructs the verified campus graph based on actual ground-truth layout."""
        # 1. Register canonical nodes
        verified_nodes = [
            ("FOUNTAIN", {"name": "Fountain", "type": "landmark", "floor": "Ground"}),
            ("JUNCTION_FOUNTAIN_RIGHT", {"name": "Avenue Junction (Right from Fountain)", "type": "junction", "floor": "Ground"}),
            ("JUNCTION_FIRST_LEFT", {"name": "First Left Turn Junction", "type": "junction", "floor": "Ground"}),
            ("UDAYA_UPAHARA", {"name": "Udaya Upahara", "type": "food", "floor": "Ground"}),
            ("JUNCTION_SECOND_LEFT", {"name": "Second Left Turn Junction", "type": "junction", "floor": "Ground"}),
            ("ENGINEERING_BLOCK", {"name": "Engineering Block", "type": "academic", "floor": "Ground"}),
            ("ADMISSION_BLOCK", {"name": "Admission Block", "type": "admin", "floor": "Ground"}),
            ("REGISTRAR_OFFICE", {"name": "Office of the Registrar", "type": "office", "building": "ADMISSION_BLOCK", "floor": "1st Floor"}),
            ("CONTROLLER_EXAMINATION", {"name": "Office of Controller of Examination", "type": "office", "building": "ADMISSION_BLOCK", "floor": "Ground"}),
            ("DEAN_OFFICE_MBA", {"name": "Dean Office of MBA Department", "type": "office", "building": "ADMISSION_BLOCK", "floor": "1st Floor"}),
            ("FOOD_STALLS_ADMISSION", {"name": "Food Stalls (Subway, Hatti Kaapi, Aromas, Taj)", "type": "food", "floor": "Ground"}),
            ("JUNCTION_SPORTS_PATH", {"name": "Sports Area Turnoff", "type": "junction", "floor": "Ground"}),
            ("SPORTS_AREA", {"name": "Sports Area & Courts", "type": "sports", "floor": "Ground"}),
            ("JUNCTION_STATIONERY", {"name": "Stationery Shop Junction", "type": "junction", "floor": "Ground"}),
            ("STATIONERY", {"name": "Stationery Shop", "type": "service", "floor": "Ground"}),
            ("D_BLOCK", {"name": "D Block Entrance", "type": "academic", "floor": "Ground"}),
            ("SCHOOL_OF_DESIGN", {"name": "School of Design", "type": "academic", "building": "D_BLOCK", "floor": "5th Floor"}),
            ("JUNCTION_D_LEFT", {"name": "D Block Left Wing Junction", "type": "junction", "floor": "Ground"}),
            ("E_BLOCK", {"name": "E Block", "type": "academic", "floor": "Ground"}),
            ("RD_CENTRE", {"name": "Research and Development Centre", "type": "research", "building": "E_BLOCK", "floor": "Ground & 1st Floor"}),
            ("F_BLOCK", {"name": "F Block", "type": "academic", "floor": "Ground"}),
            ("L_BLOCK", {"name": "L Block", "type": "academic", "floor": "Ground"}),
            ("SCHOOL_OF_MEDIA_STUDIES", {"name": "School of Media Studies", "type": "academic", "building": "L_BLOCK", "floor": "Ground"}),
            ("DEAN_OFFICE_L_BLOCK", {"name": "Dean's Office (L Block)", "type": "office", "building": "L_BLOCK", "floor": "1st Floor"}),
            ("FOOD_STALLS_L_BLOCK", {"name": "Food Stalls (V Mart, Crazy Cups, Lassi Area)", "type": "food", "floor": "Ground"}),
            ("H_BLOCK", {"name": "H Block", "type": "academic", "building": "ENGINEERING_BLOCK", "floor": "Ground"}),
            ("J_BLOCK", {"name": "J Block", "type": "academic", "building": "ENGINEERING_BLOCK", "floor": "Ground"}),
            ("K_BLOCK", {"name": "K Block", "type": "academic", "building": "ENGINEERING_BLOCK", "floor": "Ground"}),
            ("N_BLOCK", {"name": "N Block", "type": "academic", "floor": "Ground"}),
            ("P_BLOCK", {"name": "P Block", "type": "academic", "floor": "Ground"}),
            ("Q_BLOCK", {"name": "Q Block", "type": "academic", "floor": "Ground"}),
            ("R_BLOCK", {"name": "R Block", "type": "academic", "floor": "Ground"}),
            ("S_BLOCK", {"name": "S Block", "type": "academic", "floor": "Ground"}),
            ("SCHOOL_OF_LAW", {"name": "School of Law", "type": "academic", "building": "S_BLOCK", "floor": "5th Floor"}),
            ("U_BLOCK", {"name": "U Block", "type": "academic", "floor": "Ground"}),
            ("AMPHITHEATER", {"name": "Amphitheater", "type": "landmark", "floor": "Ground"}),
            ("AUDITORIUM", {"name": "Auditorium", "type": "facility", "floor": "Ground"}),
            ("CENTRAL_LIBRARY", {"name": "Central Library", "type": "facility", "floor": "Ground"}),
            ("DOMINOS", {"name": "Domino's Pizza", "type": "food", "floor": "Ground"})
        ]

        for node_id, attrs in verified_nodes:
            self.graph.add_node(node_id, **attrs)
            self.node_metadata[node_id] = attrs

        # 2. Add verified pedestrian edges with distances, turn instructions, and landmarks
        verified_edges = [
            # Fountain to right spine
            ("FOUNTAIN", "JUNCTION_FOUNTAIN_RIGHT", {
                "distance_m": 15,
                "turn_instruction": "From Fountain, take a right onto the main campus avenue.",
                "landmark": "Campus Fountain",
                "verified": True
            }),
            # Avenue spine to First Left (Udaya Upahara)
            ("JUNCTION_FOUNTAIN_RIGHT", "JUNCTION_FIRST_LEFT", {
                "distance_m": 25,
                "turn_instruction": "Walk straight along the avenue to the first left opening.",
                "landmark": "Landscaped palm walkway",
                "verified": True
            }),
            ("JUNCTION_FIRST_LEFT", "UDAYA_UPAHARA", {
                "distance_m": 20,
                "turn_instruction": "Take the first left turn towards Udaya Upahara dining area.",
                "landmark": "Udaya Upahara signage",
                "verified": True
            }),
            # Avenue spine to Second Left (Engineering & Admission Block)
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
            ("ENGINEERING_BLOCK", "ADMISSION_BLOCK", {
                "distance_m": 15,
                "turn_instruction": "Walk right beside the Engineering Block to reach the Admission Block.",
                "landmark": "Admission Block entrance atrium",
                "verified": True
            }),
            # Vertical access inside Admission Block: Registrar Office on 1st Floor
            ("ADMISSION_BLOCK", "REGISTRAR_OFFICE", {
                "distance_m": 10,
                "turn_instruction": "Inside Admission Block, take the stairs or elevator to the 1st floor to reach the Office of the Registrar.",
                "landmark": "Registrar Office sign (Counter-01, 02, 03)",
                "is_vertical": True,
                "verified": True
            }),
            ("ADMISSION_BLOCK", "CONTROLLER_EXAMINATION", {
                "distance_m": 10,
                "turn_instruction": "Walk past the ground floor reception of Admission Block to the Controller of Examination counters.",
                "landmark": "Exam branch counter sign",
                "verified": True
            }),
            ("ADMISSION_BLOCK", "DEAN_OFFICE_MBA", {
                "distance_m": 15,
                "turn_instruction": "Inside Admin Block, take the stairs or elevator to the 1st floor to reach the Dean Office of MBA Department.",
                "landmark": "Dean Office MBA signage",
                "is_vertical": True,
                "verified": True
            }),
            # Opposite Admission Block are Food Stalls (Subway, Hatti Kaapi, Aromas, Taj Delight)
            ("ADMISSION_BLOCK", "FOOD_STALLS_ADMISSION", {
                "distance_m": 20,
                "turn_instruction": "Cross directly opposite the Admission Block to the covered food stalls arcade.",
                "landmark": "Subway & Hatti Kaapi stalls",
                "verified": True
            }),
            ("JUNCTION_SECOND_LEFT", "FOOD_STALLS_ADMISSION", {
                "distance_m": 25,
                "turn_instruction": "Continue straight; on your right side you will see the food stalls opposite Admission Block.",
                "landmark": "Food court signboards",
                "verified": True
            }),
            # Food stalls pathway leading to Sports Area on right side
            ("FOOD_STALLS_ADMISSION", "JUNCTION_SPORTS_PATH", {
                "distance_m": 30,
                "turn_instruction": "Walk into the food stalls corridor and follow the path extending toward the right.",
                "landmark": "Outdoor food seating",
                "verified": True
            }),
            ("JUNCTION_SPORTS_PATH", "SPORTS_AREA", {
                "distance_m": 40,
                "turn_instruction": "Follow the path on the right into the open athletic complex with basketball, volleyball, throwball, football courts, and gym.",
                "landmark": "Basketball and sports courts fencing",
                "verified": True
            }),
            # Straight path from Admission Block to D Block near Stationery
            ("ADMISSION_BLOCK", "JUNCTION_STATIONERY", {
                "distance_m": 35,
                "turn_instruction": "Head straight ahead past Admission Block toward the Stationery shop.",
                "landmark": "Stationery shop building",
                "verified": True
            }),
            ("JUNCTION_STATIONERY", "STATIONERY", {
                "distance_m": 10,
                "turn_instruction": "Turn slightly right to enter the campus stationery and photocopy store.",
                "landmark": "Stationery & supplies shop",
                "verified": True
            }),
            ("JUNCTION_STATIONERY", "D_BLOCK", {
                "distance_m": 15,
                "turn_instruction": "Continue straight past the stationery shop into D Block main entrance.",
                "landmark": "D Block Entrance foyer",
                "verified": True
            }),
            # Vertical access in D Block to 5th floor School of Design
            ("D_BLOCK", "SCHOOL_OF_DESIGN", {
                "distance_m": 15,
                "turn_instruction": "Inside D Block, take the stairs or elevator to the 5th floor. The School of Design is located on the entire fifth floor.",
                "landmark": "Blue SCHOOL OF DESIGN overhead signage",
                "is_vertical": True,
                "verified": True
            }),
            # Left from D Block leads to E, F, L blocks
            ("D_BLOCK", "JUNCTION_D_LEFT", {
                "distance_m": 20,
                "turn_instruction": "Take the left corridor exiting from D Block.",
                "landmark": "D Block west connector",
                "verified": True
            }),
            ("JUNCTION_D_LEFT", "E_BLOCK", {
                "distance_m": 30,
                "turn_instruction": "Walk ahead along the covered wing to reach E Block (E Block Seminar Hall on left).",
                "landmark": "E Block Seminar Hall",
                "verified": True
            }),
            # E Block houses R&D Centre on Ground and 1st floor
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
            ("F_BLOCK", "L_BLOCK", {
                "distance_m": 35,
                "turn_instruction": "Walk straight through F Block corridor which directly leads to L Block.",
                "landmark": "L Block entrance concourse",
                "verified": True
            }),
            # L Block ground floor has School of Media Studies, 1st floor has Dean's Office
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
            # Food stalls near L Block: Hatti Kaapi, V Mart, Crazy Cups, Lassi Area
            ("L_BLOCK", "FOOD_STALLS_L_BLOCK", {
                "distance_m": 20,
                "turn_instruction": "Step out to the left of L Block to reach the food stalls arcade featuring V Mart, Crazy Cups, Hatti Kaapi, and Lassi Area.",
                "landmark": "Crazy Cups and VJ Mart stalls",
                "verified": True
            }),
            # Inside Engineering Block: H, J, K leading to N, P, Q, R, S, U
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
            # Coming from N to P, food stalls are on the right side
            ("P_BLOCK", "FOOD_STALLS_L_BLOCK", {
                "distance_m": 15,
                "turn_instruction": "On the right side of P Block, you can access the food stalls (Hatti Kaapi, V Mart, Crazy Cups, Lassi Area).",
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
            # S Block 5th floor houses School of Law
            ("S_BLOCK", "SCHOOL_OF_LAW", {
                "distance_m": 15,
                "turn_instruction": "Inside S Block, take the elevator or staircase to the 5th floor. The School of Law is located on the fifth floor.",
                "landmark": "School of Law plaque & Law Library",
                "is_vertical": True,
                "verified": True
            }),
            ("S_BLOCK", "U_BLOCK", {
                "distance_m": 25,
                "turn_instruction": "Walk past S Block to reach U Block at the end of the academic complex.",
                "landmark": "U Block terminal",
                "verified": True
            }),
            # Amphitheater & Auditorium connections
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
            ("JUNCTION_SPORTS_PATH", "DOMINOS", {
                "distance_m": 25,
                "turn_instruction": "Walk past the cafeteria pavilion towards the Domino's pizza outlet kiosk.",
                "landmark": "Domino's red and blue logo",
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
        
        # Check alias dictionary
        alias_map = {
            "fountain": "FOUNTAIN",
            "campus fountain": "FOUNTAIN",
            "central fountain": "FOUNTAIN",
            "udaya": "UDAYA_UPAHARA",
            "udaya upahara": "UDAYA_UPAHARA",
            "udaya upahar": "UDAYA_UPAHARA",
            "engineering block": "ENGINEERING_BLOCK",
            "engg block": "ENGINEERING_BLOCK",
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
            "food stalls": "FOOD_STALLS_ADMISSION",
            "food court": "FOOD_STALLS_ADMISSION",
            "subway": "FOOD_STALLS_ADMISSION",
            "hatti kaapi": "FOOD_STALLS_ADMISSION",
            "taj delight": "FOOD_STALLS_ADMISSION",
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
            "research and development centre": "RD_CENTRE",
            "f block": "F_BLOCK",
            "l block": "L_BLOCK",
            "school of media studies": "SCHOOL_OF_MEDIA_STUDIES",
            "media studies": "SCHOOL_OF_MEDIA_STUDIES",
            "tv studio": "SCHOOL_OF_MEDIA_STUDIES",
            "dean office": "DEAN_OFFICE_L_BLOCK",
            "v mart": "FOOD_STALLS_L_BLOCK",
            "vj mart": "FOOD_STALLS_L_BLOCK",
            "crazy cups": "FOOD_STALLS_L_BLOCK",
            "lassi area": "FOOD_STALLS_L_BLOCK",
            "lassi house": "FOOD_STALLS_L_BLOCK",
            "sports": "SPORTS_AREA",
            "sports area": "SPORTS_AREA",
            "sports complex": "SPORTS_AREA",
            "basketball court": "SPORTS_AREA",
            "volleyball court": "SPORTS_AREA",
            "gym": "SPORTS_AREA",
            "indoor games": "SPORTS_AREA",
            "n block": "N_BLOCK",
            "p block": "P_BLOCK",
            "q block": "Q_BLOCK",
            "r block": "R_BLOCK",
            "s block": "S_BLOCK",
            "school of law": "SCHOOL_OF_LAW",
            "law school": "SCHOOL_OF_LAW",
            "u block": "U_BLOCK",
            "dominos": "DOMINOS",
            "amphitheater": "AMPHITHEATER",
            "auditorium": "AUDITORIUM"
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
            # Shortest path using verified edges
            path = nx.shortest_path(self.graph, source=source_id, target=dest_id, weight=weight)
            
            steps = []
            total_dist = 0
            landmarks_seen = []

            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                edge_data = self.graph.get_edge_data(u, v)
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
                "error": f"No verified traversable path connects {source_id} and {dest_id}.",
                "clarification_needed": False,
                "route": [],
                "steps": [],
                "total_distance_m": 0
            }

    def generate_natural_directions(self, route_result: Dict[str, Any]) -> str:
        """Converts graph route result into natural language directions."""
        if not route_result.get("success"):
            return route_result.get("error", "Unable to compute route.")

        if route_result.get("is_same_location"):
            return route_result["steps"][0]

        source_name = route_result["source_name"]
        dest_name = route_result["destination_name"]
        total_dist = route_result["total_distance_m"]
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
