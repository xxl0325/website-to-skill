#!/usr/bin/env python3
"""Convert DESIGN.md reference to SKILL.md and refined DESIGN.md."""

import argparse
import json
from pathlib import Path

from converter.llm_analyzer import analyze_with_llm, generate_skill_content, generate_design_content


def main():
    parser = argparse.ArgumentParser(
        description="Convert DESIGN.md reference to SKILL.md"
    )
    parser.add_argument(
        "input",
        help="Path to input DESIGN.md file"
    )
    parser.add_argument(
        "--name", required=True, help="Name for the generated skill"
    )
    parser.add_argument(
        "--output",
        default="./output",
        help="Output directory for generated skill"
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-5-20251122",
        help="Model to use for analysis"
    )
    args = parser.parse_args()

    print(f"Reading {args.input}...")
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {args.input} does not exist")
        return

    design_content = input_path.read_text()

    print(f"Analyzing with LLM ({args.model})...")
    extracted_data = analyze_with_llm(design_content, args.model)

    print(f"Generating skill: {args.name}")
    output_dir = Path(args.output) / args.name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate SKILL.md
    skill_content = generate_skill_content(args.name, extracted_data)
    skill_path = output_dir / "SKILL.md"
    skill_path.write_text(skill_content)
    print(f"  - Created {skill_path}")

    # Generate references/design.md
    references_dir = output_dir / "references"
    references_dir.mkdir(parents=True, exist_ok=True)
    design_output = generate_design_content(args.name, extracted_data)
    design_path = references_dir / "design.md"
    design_path.write_text(design_output)
    print(f"  - Created {design_path}")

    print(f"Done! Output saved to {output_dir}/")


if __name__ == "__main__":
    main()
