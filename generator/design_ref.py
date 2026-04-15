"""Generate references/design.md file from design data."""

import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from scraper.analyzer import DesignData


def generate_design_ref(name: str, design: DesignData, output_dir: str) -> str:
    """
    Generate references/design.md file.

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
    template = env.get_template("DESIGN.md.j2")

    # Prepare context
    brand_name = name.capitalize()

    context = {
        "name": name,
        "brand_name": brand_name,
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
    references_dir = Path(output_dir) / name / "references"
    references_dir.mkdir(parents=True, exist_ok=True)

    output_path = references_dir / "design.md"
    output_path.write_text(content)

    return str(output_path)
