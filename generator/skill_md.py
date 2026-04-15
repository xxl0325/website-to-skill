"""Generate SKILL.md file from design data."""

import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from scraper.analyzer import DesignData


def generate_skill(name: str, design: DesignData, output_dir: str) -> str:
    """
    Generate SKILL.md file.

    Args:
        name: Skill name
        design: Extracted design data
        output_dir: Output directory

    Returns:
        Path to generated file
    """
    # Set up Jinja2 environment
    template_dir = Path(__file__).parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))

    # Load template
    template = env.get_template("SKILL.md.j2")

    # Prepare context
    brand_name = name.capitalize()
    visual_identity = generate_visual_identity(design)

    context = {
        "name": name,
        "brand_name": brand_name,
        "visual_identity": visual_identity,
        "colors": design.colors,
        "fonts": design.fonts,
        "buttons": design.buttons,
        "spacing": design.spacing,
        "border_radius": design.border_radius,
        "shadows": design.shadows,
    }

    # Render template
    content = template.render(context)

    # Write file
    output_path = Path(output_dir) / name / "SKILL.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)

    return str(output_path)


def generate_visual_identity(design: DesignData) -> str:
    """Generate visual identity description."""
    descriptions = []

    if design.colors.get("primary"):
        descriptions.append(
            f"Primary color is {design.colors['primary']}."
        )

    if design.fonts.get("family"):
        descriptions.append(
            f"Uses {design.fonts['family']} typography."
        )

    if design.border_radius.get("default"):
        radius = design.border_radius["default"]
        if "0" in radius:
            descriptions.append("Sharp, minimal border radius.")
        else:
            descriptions.append(f"Rounded corners with {radius} radius.")

    return " ".join(descriptions) or "Clean, modern design aesthetic."
