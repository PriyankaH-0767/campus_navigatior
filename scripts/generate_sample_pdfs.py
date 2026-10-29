"""
Generates the official campus_directions.pdf and campus_images.pdf
to complete the end-to-end multimodal PDF repository.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_directions_pdf(filepath="data/campus_directions.pdf"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, leading=24, textColor=colors.HexColor('#1e3c72'))
    h2_style = ParagraphStyle('H2Style', parent=styles['Heading2'], fontSize=14, leading=18, textColor=colors.HexColor('#2a5298'))
    body_style = ParagraphStyle('BodyStyle', parent=styles['BodyText'], fontSize=11, leading=16, textColor=colors.HexColor('#2f3542'))
    
    story = [
        Paragraph("Campus Navigation and Directions Guide", title_style),
        Paragraph("<b>Document Reference:</b> CAMPUS-DIR-2026-V1 &bull; Verified Pedestrian Connections", body_style),
        Spacer(1, 15),
        
        Paragraph("Page 1: Entrance, Central Fountain & Engineering Wing", h2_style),
        Spacer(1, 8),
        Paragraph("From fountain take right.<br/><br/>"
                  "If you take first left you reach <b>'udaya upahara'</b>.<br/>"
                  "If you take second left you find <b>engineering block</b> and beside that is the <b>admission block</b>; "
                  "in the same building in the first floor you can find <b>'office of registrar'</b>.<br/>"
                  "If you go inside the engineering block you find <b>H, J, K</b> and it leads to <b>N, P, Q, R, S, U</b> blocks.<br/>"
                  "If you take exact straight path after left from fountain in the right side you find food stalls opposite to admission block such as "
                  "<b>'Subway'</b>, <b>'hatti kaapi'</b>, <b>'aromas of malenadu'</b>, <b>'taj delight'</b>.", body_style),
        Spacer(1, 20),
        PageBreak(),
        
        Paragraph("Page 2: D Block, Seminar Halls, R&D Centre & Sports Facilities", h2_style),
        Spacer(1, 8),
        Paragraph("If head straight from admission block to find the <b>'D block'</b> near the <b>'stationary'</b>.<br/>"
                  "If take left from D block you lead to <b>E, F, L blocks</b>; in the left you find E and F block seminar halls.<br/>"
                  "In ground floor and in first floor of E block you find the <b>'research and development centre'</b>.<br/>"
                  "In D block fifth floor is the <b>'School of design'</b>.<br/><br/>"
                  "If you walk into the food stalls you find a way to sports area in the right side: "
                  "<b>basketball court</b>, <b>throw ball court</b>, <b>volleyball court</b>, <b>football courts</b> and the <b>sports room</b>.", body_style),
        Spacer(1, 20),
        PageBreak(),
        
        Paragraph("Page 3: F Block, L Block, Southern Spine & School of Law", h2_style),
        Spacer(1, 8),
        Paragraph("F block leads to L block; in L block in your left again there are food stalls: "
                  "<b>'hatti kaapi'</b>, <b>'v mart'</b>, <b>'crazy cups'</b>, <b>'lassi area'</b>.<br/>"
                  "First floor has <b>dean office</b>; ground floor houses <b>School of Media Studies</b>.<br/><br/>"
                  "These food stalls can also be found when you come from N to P, in P block right side.<br/>"
                  "P leads to Q and then R and S, U blocks.<br/>"
                  "S block 5th floor you find <b>'School of law'</b>.", body_style)
    ]
    doc.build(story)
    print(f"Generated {filepath} successfully.")

def generate_images_pdf(filepath="data/campus_images.pdf"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, leading=22, textColor=colors.HexColor('#1e3c72'))
    h2_style = ParagraphStyle('H2Style', parent=styles['Heading2'], fontSize=13, leading=16, textColor=colors.HexColor('#2a5298'))
    cell_style = ParagraphStyle('CellStyle', parent=styles['Normal'], fontSize=9, leading=12)

    story = [
        Paragraph("Labeled Campus Photographs Catalogue", title_style),
        Paragraph("Verified Ground-Truth Photographic Records &bull; 8 Pages", cell_style),
        Spacer(1, 15)
    ]

    pages_data = [
        ("Page 1: Administrative Complex & Offices", [
            ("Office of controller examination", "Admin block"),
            ("Dean office of MBA department", "Nexus core"),
            ("Office of International Affairs", "Fee department")
        ]),
        ("Page 2: Student Services & Libraries", [
            ("Café (Café Feasto)", "ATM"),
            ("Library (Reading Hall)", "Medical room (Manipal Clinics)"),
            ("Library (Book Stacks)", "Computer lab")
        ]),
        ("Page 3: Cultural & Event Facilities", [
            ("Musical room", "DSA (Student Affairs)"),
            ("DSA (Central Concourse)", "Amphitheater"),
            ("Cafeteria Terrace", "Campus Auditorium")
        ]),
        ("Page 4: Academic Wings & Outlets", [
            ("M block (Classrooms MG: 01-13)", "Domino's Pizza"),
            ("Transport department", "Lassi house")
        ]),
        ("Page 5: Creative & Advanced Technology Studios", [
            ("School of design (D Block 5th Floor)", "Full stack development lab"),
            ("VR Studio", "AI centre of excellence (NVIDIA)")
        ]),
        ("Page 6: Governance, Civil Engineering & Legal Faculty", [
            ("Indoor games (Table Tennis)", "VJ Mart"),
            ("Office of registrar (Counters 01-03)", "Department of civil engineering"),
            ("School of law (S Block 5th Floor)", "Dean office PSCS")
        ]),
        ("Page 7: Athletic & Food Outlets", [
            ("Gym (Fitness Centre)", "Law Library"),
            ("Udaya Upahar (उदय ಉಪಹಾರ)", "Hatti Kaapi (Traditional Coffee)")
        ]),
        ("Page 8: Media Studios & Kiosks", [
            ("School of Media Studies / TV Studio", "Crazy Cups Snack Kiosk")
        ])
    ]

    for p_idx, (p_title, rows) in enumerate(pages_data):
        story.append(Paragraph(f"<b>{p_title}</b>", h2_style))
        story.append(Spacer(1, 8))
        
        table_data = []
        for r in rows:
            if len(r) == 2:
                table_data.append([
                    Paragraph(f"<b>[PHOTO]</b> {r[0]}", cell_style),
                    Paragraph(f"<b>[PHOTO]</b> {r[1]}", cell_style)
                ])
            else:
                table_data.append([Paragraph(f"<b>[PHOTO]</b> {r[0]}", cell_style)])

        t = Table(table_data, colWidths=[250, 250])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f2f6')),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#ced6e0')),
            ('PADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t)
        story.append(Spacer(1, 15))
        if p_idx < len(pages_data) - 1:
            story.append(PageBreak())

    doc.build(story)
    print(f"Generated {filepath} successfully.")

if __name__ == "__main__":
    generate_directions_pdf()
    generate_images_pdf()
