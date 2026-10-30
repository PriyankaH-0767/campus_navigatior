import networkx as nx

def build_test_graph():
    g = nx.Graph()

    # All 64 canonical places, landmarks, facilities, and academic wings
    nodes = [
        ("UNIVERSITY_ENTRANCE", {"name": "University Entrance Gate", "type": "entrance", "floor": "Ground"}),
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
        ("SPORTS_AREA", {"name": "Sports Area and Outdoor Courts", "type": "sports", "floor": "Ground"}),
        ("INDOOR_GAMES", {"name": "Indoor Games Hall", "type": "sports", "floor": "Ground"}),
        ("GYM", {"name": "Campus Fitness Gym", "type": "sports", "floor": "Ground"}),
        ("DOMINOS", {"name": "Domino's Pizza", "type": "food", "floor": "Ground"}),
        ("CENTRAL_LIBRARY", {"name": "Central Campus Library", "type": "facility", "floor": "Ground and 1st"}),
        ("CAFETERIA", {"name": "Central Cafeteria", "type": "food", "floor": "Ground"}),
        ("AMPHITHEATER", {"name": "Amphitheater", "type": "landmark", "floor": "Ground"}),
        ("AUDITORIUM", {"name": "Main Auditorium", "type": "facility", "floor": "Ground"}),
        ("DSA_OFFICE", {"name": "DSA Office", "type": "office", "floor": "Ground"}),
        ("MUSICAL_ROOM", {"name": "Musical Room", "type": "facility", "floor": "Ground"}),
        ("MEDICAL_ROOM", {"name": "Medical Room (Manipal Clinics)", "type": "service", "floor": "Ground"}),
        ("TRANSPORT_DEPARTMENT", {"name": "Transport Department", "type": "office", "floor": "Ground"}),
        ("M_BLOCK", {"name": "M Block", "type": "academic", "floor": "Ground"}),
        ("JUNCTION_STATIONERY", {"name": "Stationery Junction", "type": "junction", "floor": "Ground"}),
        ("STATIONERY", {"name": "Stationery and Photocopy Shop", "type": "service", "floor": "Ground"}),
        ("D_BLOCK", {"name": "D Block Entrance", "type": "academic", "floor": "Ground"}),
        ("SCHOOL_OF_DESIGN", {"name": "School of Design", "type": "academic", "floor": "5th Floor"}),
        ("JUNCTION_D_LEFT", {"name": "D Block West Junction", "type": "junction", "floor": "Ground"}),
        ("E_BLOCK", {"name": "E Block", "type": "academic", "floor": "Ground"}),
        ("RD_CENTRE", {"name": "Research and Development Centre", "type": "research", "floor": "Ground and 1st"}),
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

    for n, attrs in nodes:
        g.add_node(n, **attrs)

    edges = [
        # Main Entrance to Fountain
        ("UNIVERSITY_ENTRANCE", "FOUNTAIN", {"distance_m": 40, "turn_instruction": "From University Entrance, walk straight along the palm tree driveway to reach the central Campus Fountain.", "landmark": "Main Entrance Palm Driveway"}),
        
        # Fountain to right avenue
        ("FOUNTAIN", "JUNCTION_FOUNTAIN_RIGHT", {"distance_m": 15, "turn_instruction": "From Fountain, take a right onto the main campus avenue.", "landmark": "Campus Fountain"}),
        ("JUNCTION_FOUNTAIN_RIGHT", "JUNCTION_FIRST_LEFT", {"distance_m": 25, "turn_instruction": "Walk straight along the avenue to the first left opening.", "landmark": "Landscaped palm walkway"}),
        ("JUNCTION_FIRST_LEFT", "UDAYA_UPAHARA", {"distance_m": 20, "turn_instruction": "Take the first left turn towards Udaya Upahar dining area.", "landmark": "Udaya Upahar signage"}),
        
        # Avenue to Engineering & Admission Complex
        ("JUNCTION_FIRST_LEFT", "JUNCTION_SECOND_LEFT", {"distance_m": 35, "turn_instruction": "Continue straight along the avenue to the second left turn.", "landmark": "Campus central trees"}),
        ("JUNCTION_SECOND_LEFT", "ENGINEERING_BLOCK", {"distance_m": 20, "turn_instruction": "Turn left at the second opening into the Engineering Block entrance.", "landmark": "Engineering Block portico"}),
        ("ENGINEERING_BLOCK", "CIVIL_DEPARTMENT", {"distance_m": 15, "turn_instruction": "Inside Engineering Block, take the ground corridor to Department of Civil Engineering.", "landmark": "Civil Engineering wing plaque"}),
        ("ENGINEERING_BLOCK", "COMPUTER_LAB", {"distance_m": 20, "turn_instruction": "Proceed along the engineering concourse to the Central Computer Lab.", "landmark": "Computer Lab glass doors"}),
        ("ENGINEERING_BLOCK", "FULL_STACK_LAB", {"distance_m": 25, "turn_instruction": "Head towards the computing labs corridor to enter the Full Stack Development Lab.", "landmark": "Full Stack Lab entrance"}),
        ("ENGINEERING_BLOCK", "AI_CENTRE_OF_EXCELLENCE", {"distance_m": 30, "turn_instruction": "Walk to the advanced technology wing to reach the AI Centre of Excellence.", "landmark": "NVIDIA AI Centre of Excellence plaque"}),
        ("ENGINEERING_BLOCK", "VR_STUDIO", {"distance_m": 30, "turn_instruction": "Walk past the AI centre to reach the VR Studio.", "landmark": "VR Studio sign"}),
        
        # Admission / Admin Complex
        ("ENGINEERING_BLOCK", "ADMISSION_BLOCK", {"distance_m": 15, "turn_instruction": "Walk right beside the Engineering Block to reach the Admission Block.", "landmark": "Admission Block entrance atrium"}),
        ("ADMISSION_BLOCK", "REGISTRAR_OFFICE", {"distance_m": 10, "turn_instruction": "Inside Admission Block, take the stairs or elevator to the 1st floor for the Office of the Registrar.", "landmark": "Registrar Office sign (Counter-01, 02, 03)", "is_vertical": True}),
        ("ADMISSION_BLOCK", "CONTROLLER_EXAMINATION", {"distance_m": 10, "turn_instruction": "Walk past the reception of Admission Block to the Controller of Examination counters.", "landmark": "Exam branch counter sign"}),
        ("ADMISSION_BLOCK", "DEAN_OFFICE_MBA", {"distance_m": 15, "turn_instruction": "Inside Admin Block, take the stairs to the 1st floor to reach the Dean Office of MBA Department.", "landmark": "Dean Office MBA signage", "is_vertical": True}),
        ("ADMISSION_BLOCK", "FEE_DEPARTMENT", {"distance_m": 10, "turn_instruction": "On the ground floor of Admin Block, head to the Fee Department counters.", "landmark": "Fee Department counter glass"}),
        ("ADMISSION_BLOCK", "OFFICE_INTERNATIONAL_AFFAIRS", {"distance_m": 12, "turn_instruction": "Walk to the dedicated lounge on the ground floor for Office of International Affairs.", "landmark": "Office of International Affairs blue board"}),
        ("ADMISSION_BLOCK", "CAMPUS_ATM", {"distance_m": 15, "turn_instruction": "Step outside Admission Block along the sidewalk to the 24/7 ATM kiosk.", "landmark": "Campus 24-Hour ATM"}),
        ("ADMISSION_BLOCK", "FOOD_STALLS_ADMISSION", {"distance_m": 20, "turn_instruction": "Cross directly opposite the Admission Block to the food stalls arcade.", "landmark": "Subway & Hatti Kaapi stalls"}),
        ("FOOD_STALLS_ADMISSION", "CAFE_FEASTO", {"distance_m": 10, "turn_instruction": "Inside the food stalls arcade, walk to Cafe Feasto.", "landmark": "Cafe Feasto counter"}),
        ("FOOD_STALLS_ADMISSION", "HATTI_KAAPI", {"distance_m": 10, "turn_instruction": "Inside the food stalls arcade, walk to Hatti Kaapi.", "landmark": "Hatti Kaapi kiosk"}),
        ("JUNCTION_SECOND_LEFT", "FOOD_STALLS_ADMISSION", {"distance_m": 25, "turn_instruction": "Continue straight; on your right side you will see the food stalls opposite Admission Block.", "landmark": "Food court signboards"}),
        
        # Sports Complex & Domino's
        ("FOOD_STALLS_ADMISSION", "JUNCTION_SPORTS_PATH", {"distance_m": 30, "turn_instruction": "Walk into the food stalls corridor and follow the path extending toward the right.", "landmark": "Outdoor food seating"}),
        ("JUNCTION_SPORTS_PATH", "SPORTS_AREA", {"distance_m": 40, "turn_instruction": "Follow the path on the right into the open athletic sports courts.", "landmark": "Sports courts fencing"}),
        ("SPORTS_AREA", "INDOOR_GAMES", {"distance_m": 15, "turn_instruction": "Enter the sports building to reach the tournament Indoor Games Hall.", "landmark": "Indoor table tennis hall"}),
        ("SPORTS_AREA", "GYM", {"distance_m": 20, "turn_instruction": "Walk to the fitness pavilion inside the sports building to reach the Campus Gym.", "landmark": "Campus Gym equipment"}),
        ("JUNCTION_SPORTS_PATH", "DOMINOS", {"distance_m": 25, "turn_instruction": "Walk past the food pavilion towards the Domino's pizza outlet kiosk.", "landmark": "Domino's red and blue logo"}),
        
        # Facilities & West Concourse
        ("ADMISSION_BLOCK", "AMPHITHEATER", {"distance_m": 45, "turn_instruction": "Walk through the landscaped central terrace to the open-air Amphitheater.", "landmark": "Green tiered steps"}),
        ("AMPHITHEATER", "AUDITORIUM", {"distance_m": 30, "turn_instruction": "Walk past the amphitheater gardens to the grand steps of the Auditorium.", "landmark": "Auditorium marble steps"}),
        ("AMPHITHEATER", "CAFETERIA", {"distance_m": 35, "turn_instruction": "Walk past the open lawn into the Central Student Cafeteria.", "landmark": "Central Cafeteria entrance"}),
        ("ADMISSION_BLOCK", "CENTRAL_LIBRARY", {"distance_m": 40, "turn_instruction": "Walk past the central garden walkway to enter the Central Campus Library.", "landmark": "Central Library entrance turnstiles"}),
        ("CENTRAL_LIBRARY", "MEDICAL_ROOM", {"distance_m": 20, "turn_instruction": "Next to the library entrance, step into the Campus Medical Room (Manipal Clinics).", "landmark": "Manipal Clinics Medical Room"}),
        ("CENTRAL_LIBRARY", "DSA_OFFICE", {"distance_m": 25, "turn_instruction": "Walk along the shaded veranda to reach the DSA Office.", "landmark": "DSA Office entrance"}),
        ("DSA_OFFICE", "MUSICAL_ROOM", {"distance_m": 20, "turn_instruction": "Walk beside the DSA courtyard to reach the Musical Room canopy.", "landmark": "Musical Room open canopy"}),
        ("ADMISSION_BLOCK", "TRANSPORT_DEPARTMENT", {"distance_m": 30, "turn_instruction": "Walk down the side concourse to the Transport Department.", "landmark": "Transport Department office"}),
        ("TRANSPORT_DEPARTMENT", "M_BLOCK", {"distance_m": 25, "turn_instruction": "Walk past the transport office to reach M Block classrooms.", "landmark": "M Block directional sign"}),
        
        # D, E, F, L Academic Wings
        ("ADMISSION_BLOCK", "JUNCTION_STATIONERY", {"distance_m": 35, "turn_instruction": "Head straight ahead past Admission Block toward the Stationery shop.", "landmark": "Stationery shop building"}),
        ("JUNCTION_STATIONERY", "STATIONERY", {"distance_m": 10, "turn_instruction": "Turn slightly right to enter the campus Stationery and photocopy shop.", "landmark": "Stationery storefront"}),
        ("JUNCTION_STATIONERY", "D_BLOCK", {"distance_m": 15, "turn_instruction": "Continue straight past the stationery shop into D Block main entrance.", "landmark": "D Block Entrance foyer"}),
        ("D_BLOCK", "SCHOOL_OF_DESIGN", {"distance_m": 15, "turn_instruction": "Inside D Block, take the stairs or elevator to the 5th floor. The School of Design is located on the entire fifth floor.", "landmark": "Blue SCHOOL OF DESIGN overhead signage", "is_vertical": True}),
        ("D_BLOCK", "JUNCTION_D_LEFT", {"distance_m": 20, "turn_instruction": "Take the left corridor exiting from D Block.", "landmark": "D Block west connector"}),
        ("JUNCTION_D_LEFT", "E_BLOCK", {"distance_m": 30, "turn_instruction": "Walk ahead along the covered wing to reach E Block.", "landmark": "E Block Seminar Hall"}),
        ("E_BLOCK", "RD_CENTRE", {"distance_m": 10, "turn_instruction": "Enter E Block; the Research and Development (R&D) Centre is situated on the ground and first floors.", "landmark": "R&D Centre and AI lab plaque", "is_vertical": True}),
        ("E_BLOCK", "F_BLOCK", {"distance_m": 25, "turn_instruction": "Proceed past E Block seminar hall to F Block.", "landmark": "F Block Seminar Hall"}),
        ("F_BLOCK", "NEXUS_CORE", {"distance_m": 20, "turn_instruction": "Pass through the Nexus Core transition underpass towards L Block.", "landmark": "NEXUS CORE overhead signage"}),
        ("NEXUS_CORE", "L_BLOCK", {"distance_m": 20, "turn_instruction": "Exit the Nexus Core passageway into the L Block entrance concourse.", "landmark": "L Block entrance concourse"}),
        ("L_BLOCK", "SCHOOL_OF_MEDIA_STUDIES", {"distance_m": 10, "turn_instruction": "On the ground floor of L Block, enter the School of Media Studies and TV Studio.", "landmark": "MEDIA STUDIES / TV STUDIO entrance"}),
        ("L_BLOCK", "DEAN_OFFICE_L_BLOCK", {"distance_m": 10, "turn_instruction": "Take the stairs to the first floor of L Block to reach the Dean's Office.", "landmark": "Dean Office notice board", "is_vertical": True}),
        ("L_BLOCK", "DEAN_OFFICE_PSCS", {"distance_m": 12, "turn_instruction": "On the first floor of L Block, walk down the corridor to Dean Office PSCS.", "landmark": "Dean Office PSCS plaque", "is_vertical": True}),
        ("L_BLOCK", "FOOD_STALLS_L_BLOCK", {"distance_m": 20, "turn_instruction": "Step out to the food stalls arcade featuring VJ Mart, Crazy Cups, and Lassi House.", "landmark": "Food stalls arcade sign"}),
        ("FOOD_STALLS_L_BLOCK", "VJ_MART", {"distance_m": 10, "turn_instruction": "Inside the food arcade, walk to VJ Mart kiosk.", "landmark": "VJ Mart kiosk"}),
        ("FOOD_STALLS_L_BLOCK", "CRAZY_CUPS", {"distance_m": 10, "turn_instruction": "Inside the food arcade, walk to Crazy Cups stall.", "landmark": "Crazy Cups kiosk"}),
        ("FOOD_STALLS_L_BLOCK", "LASSI_HOUSE", {"distance_m": 10, "turn_instruction": "Inside the food arcade, walk to Lassi House.", "landmark": "Lassi House signage"}),
        
        # Engineering Spine: H, J, K -> N, P, Q, R, S, U
        ("ENGINEERING_BLOCK", "H_BLOCK", {"distance_m": 20, "turn_instruction": "Enter Engineering Block and take the internal concourse towards H Block.", "landmark": "H Block corridor"}),
        ("H_BLOCK", "J_BLOCK", {"distance_m": 20, "turn_instruction": "Walk straight through the internal corridor from H Block to J Block.", "landmark": "J Block wing"}),
        ("J_BLOCK", "K_BLOCK", {"distance_m": 20, "turn_instruction": "Continue along the enclosed corridor from J Block to K Block.", "landmark": "K Block wing"}),
        ("K_BLOCK", "N_BLOCK", {"distance_m": 25, "turn_instruction": "Exit the K Block corridor into the N Block connector walkway.", "landmark": "N Block entrance arch"}),
        ("N_BLOCK", "P_BLOCK", {"distance_m": 35, "turn_instruction": "Follow the main pedestrian walkway from N Block to P Block.", "landmark": "P Block academic sign"}),
        ("P_BLOCK", "FOOD_STALLS_L_BLOCK", {"distance_m": 15, "turn_instruction": "On the right side of P Block, you can access the food stalls arcade.", "landmark": "P Block food pavilion"}),
        ("P_BLOCK", "Q_BLOCK", {"distance_m": 30, "turn_instruction": "Proceed south past P Block to Q Block.", "landmark": "Q Block corridor"}),
        ("Q_BLOCK", "R_BLOCK", {"distance_m": 30, "turn_instruction": "Continue along the covered passage from Q Block to R Block.", "landmark": "R Block sign"}),
        ("R_BLOCK", "S_BLOCK", {"distance_m": 35, "turn_instruction": "Walk from R Block to reach S Block entrance.", "landmark": "S Block entrance lobby"}),
        ("S_BLOCK", "SCHOOL_OF_LAW", {"distance_m": 15, "turn_instruction": "Inside S Block, take the elevator or staircase to the 5th floor for the School of Law.", "landmark": "School of Law plaque", "is_vertical": True}),
        ("SCHOOL_OF_LAW", "LAW_LIBRARY", {"distance_m": 10, "turn_instruction": "On the 5th floor of S Block, enter the dedicated Law Library.", "landmark": "Law Library entrance door"}),
        ("S_BLOCK", "U_BLOCK", {"distance_m": 25, "turn_instruction": "Walk past S Block to reach U Block at the end of the academic complex.", "landmark": "U Block terminal"})
    ]

    for u, v, attrs in edges:
        g.add_edge(u, v, **attrs)

    return g

if __name__ == "__main__":
    g = build_test_graph()
    print("Graph built successfully!")
    print(f"Total Nodes: {len(g.nodes)}")
    print(f"Total Edges: {len(g.edges)}")
    isolated = [n for n in g.nodes if g.degree(n) == 0]
    print(f"Isolated Nodes: {isolated}")
    print(f"Is graph fully connected? {nx.is_connected(g)}")
    
    # Test route from Fountain to School of Law
    path = nx.shortest_path(g, "FOUNTAIN", "SCHOOL_OF_LAW", weight="distance_m")
    print(f"Route Fountain -> Law: {' -> '.join(path)}")
    
    # Test route from Domino's to School of Design
    path2 = nx.shortest_path(g, "DOMINOS", "SCHOOL_OF_DESIGN", weight="distance_m")
    print(f"Route Dominos -> Design: {' -> '.join(path2)}")
    
    # Test nearest locations from Office of the Registrar
    lengths = nx.single_source_dijkstra_path_length(g, "REGISTRAR_OFFICE", weight="distance_m")
    nearest = [n for n in sorted(lengths.items(), key=lambda x: x[1]) if not n[0].startswith("JUNCTION_") and n[0] != "REGISTRAR_OFFICE"][:5]
    print(f"Nearest to Registrar Office: {nearest}")
