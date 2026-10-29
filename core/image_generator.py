"""
Visual Explanation & Image Generation Module
Generates illustrative campus scenes, conceptual entrance guides, and verified route diagrams.
Clearly distinguishes between illustrative visual aids and deterministic graph maps.
"""

from typing import Dict, Any, List, Optional
import html

class CampusVisualGenerator:
    def __init__(self):
        pass

    def generate_illustration(self, prompt: str, scene_type: str = "entrance") -> Dict[str, Any]:
        """
        Creates an illustrative campus conceptual scene SVG.
        Includes an unmissable watermark to guarantee non-confusion with verified maps.
        """
        p_clean = prompt.lower()
        title = "Campus Scene Illustration"
        bg_gradient_start = "#1e3c72"
        bg_gradient_end = "#2a5298"
        accent_color = "#4facfe"

        if "entrance" in p_clean:
            title = "Illustrative Campus Entrance Archway"
            elements = """
            <!-- Entrance Arch and Pillars -->
            <polygon points="120,420 120,180 180,180 180,420" fill="#ced6e0" stroke="#747d8c" stroke-width="3"/>
            <polygon points="620,420 620,180 680,180 680,420" fill="#ced6e0" stroke="#747d8c" stroke-width="3"/>
            <path d="M120,180 Q400,90 680,180 L680,130 Q400,40 120,130 Z" fill="#2ed573" stroke="#26af5f" stroke-width="3"/>
            <text x="400" y="145" font-family="Arial, sans-serif" font-size="22" font-weight="bold" fill="#ffffff" text-anchor="middle">SMART CAMPUS PORTAL</text>
            <!-- Walkway and Trees -->
            <polygon points="260,420 540,420 480,260 320,260" fill="#dfe4ea" stroke="#a4b0be" stroke-width="2"/>
            <circle cx="210" cy="280" r="45" fill="#2ed573" opacity="0.85"/>
            <rect x="202" y="280" width="16" height="60" fill="#8b5a2b"/>
            <circle cx="590" cy="280" r="45" fill="#2ed573" opacity="0.85"/>
            <rect x="582" y="280" width="16" height="60" fill="#8b5a2b"/>
            """
        elif "design" in p_clean or "d block" in p_clean:
            title = "Illustrative School of Design Studio"
            elements = """
            <rect x="150" y="160" width="500" height="230" fill="#ffffff" rx="12" stroke="#70a1ff" stroke-width="4"/>
            <rect x="180" y="200" width="120" height="150" fill="#f1f2f6" stroke="#ced6e0" stroke-width="2"/>
            <text x="240" y="275" font-family="Arial" font-size="14" fill="#57606f" text-anchor="middle">Studio Pod A</text>
            <rect x="340" y="200" width="120" height="150" fill="#f1f2f6" stroke="#ced6e0" stroke-width="2"/>
            <text x="400" y="275" font-family="Arial" font-size="14" fill="#57606f" text-anchor="middle">CAD Station</text>
            <rect x="500" y="200" width="120" height="150" fill="#f1f2f6" stroke="#ced6e0" stroke-width="2"/>
            <text x="560" y="275" font-family="Arial" font-size="14" fill="#57606f" text-anchor="middle">Model Bench</text>
            <rect x="250" y="110" width="300" height="40" fill="#1e90ff" rx="6"/>
            <text x="400" y="137" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#ffffff" text-anchor="middle">D-BLOCK 5TH FLOOR STUDIO</text>
            """
        else:
            title = "Illustrative Campus Academic Block & Walkway"
            elements = """
            <rect x="160" y="140" width="480" height="220" fill="#f5f6fa" stroke="#dcdde1" stroke-width="3" rx="8"/>
            <rect x="200" y="180" width="80" height="60" fill="#70a1ff" rx="4"/>
            <rect x="310" y="180" width="80" height="60" fill="#70a1ff" rx="4"/>
            <rect x="420" y="180" width="80" height="60" fill="#70a1ff" rx="4"/>
            <rect x="530" y="180" width="80" height="60" fill="#70a1ff" rx="4"/>
            <polygon points="280,420 520,420 460,320 340,320" fill="#e1b12c" opacity="0.6"/>
            """

        svg_content = f"""
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 460" width="100%" height="auto" style="border-radius:12px; box-shadow:0 8px 24px rgba(0,0,0,0.15);">
          <defs>
            <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="{bg_gradient_start}"/>
              <stop offset="100%" stop-color="{bg_gradient_end}"/>
            </linearGradient>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
            </pattern>
          </defs>
          <!-- Background -->
          <rect width="800" height="460" fill="url(#bgGrad)"/>
          <rect width="800" height="460" fill="url(#grid)"/>

          <!-- Title -->
          <text x="400" y="42" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#ffffff" text-anchor="middle">{title}</text>

          <!-- Scene Elements -->
          {elements}

          <!-- Strict Mandatory Watermark Banner -->
          <rect x="20" y="415" width="760" height="32" fill="#ff4757" rx="6" opacity="0.95"/>
          <text x="400" y="437" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">
            ⚠️ ILLUSTRATIVE CONCEPTUAL VISUAL AID — NOT VERIFIED ROUTE GEOMETRY
          </text>
        </svg>
        """

        return {
            "prompt": prompt,
            "scene_title": title,
            "svg_data": svg_content.strip(),
            "nature": "illustrative_visual_aid",
            "is_verified_route": False,
            "disclaimer": "This generated illustration is a conceptual visual aid and must not be used as verified navigational ground truth."
        }

    def generate_route_diagram_svg(self, route_result: Dict[str, Any]) -> str:
        """
        Renders the actual verified NetworkX graph path into a high-contrast visual diagram.
        Every single segment corresponds to mathematically verified graph edges.
        """
        if not route_result.get("success"):
            return ""

        route_nodes = route_result.get("route", [])
        if not route_nodes:
            return ""

        node_count = len(route_nodes)
        width = max(800, node_count * 150)
        height = 220
        spacing = (width - 160) / max(1, node_count - 1)

        node_elements = []
        for i, node_id in enumerate(route_nodes):
            cx = 80 + i * spacing
            cy = 100
            
            # Connections line
            if i < node_count - 1:
                next_cx = 80 + (i + 1) * spacing
                node_elements.append(
                    f'<line x1="{cx}" y1="{cy}" x2="{next_cx}" y2="{cy}" stroke="#00d2d3" stroke-width="6" stroke-dasharray="8 4"/>'
                    f'<polygon points="{next_cx-12},{cy-8} {next_cx},{cy} {next_cx-12},{cy+8}" fill="#00d2d3"/>'
                )

            # Node bubble
            fill_color = "#10ac84" if (i == 0 or i == node_count - 1) else "#2e86de"
            tag = "START" if i == 0 else ("DESTINATION" if i == node_count - 1 else f"WAYPOINT {i}")
            
            clean_name = node_id.replace("_", " ")
            if len(clean_name) > 16:
                clean_name = clean_name[:14] + ".."

            node_elements.append(f"""
            <circle cx="{cx}" cy="{cy}" r="26" fill="{fill_color}" stroke="#ffffff" stroke-width="4"/>
            <text x="{cx}" y="{cy-35}" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#ff9f43" text-anchor="middle">{tag}</text>
            <text x="{cx}" y="{cy+5}" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">{i+1}</text>
            <text x="{cx}" y="{cy+48}" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">{clean_name}</text>
            """)

        svg = f"""
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto" style="background:#1e272e; border-radius:10px; margin-top:12px; padding:10px;">
          <!-- Header Banner -->
          <rect x="20" y="15" width="{width-40}" height="30" fill="#222f3e" rx="6"/>
          <text x="{width/2}" y="35" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#10ac84" text-anchor="middle">
            ✅ VERIFIED ROUTE TOPOLOGY (Generated from Deterministic NetworkX Graph)
          </text>
          
          <!-- Route graph path -->
          {' '.join(node_elements)}
        </svg>
        """
        return svg.strip()
