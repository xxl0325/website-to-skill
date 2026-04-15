#!/usr/bin/env python3
"""Generate DESIGN.md from website URL or local HTML file using LLM analysis."""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Generate DESIGN.md from website URL or local HTML file"
    )
    parser.add_argument(
        "input",
        help="Website URL or path to local HTML file"
    )
    parser.add_argument(
        "--name", required=True, help="Name for the design system"
    )
    parser.add_argument(
        "--output",
        default="./output",
        help="Output directory for generated files",
    )
    parser.add_argument(
        "--css",
        help="Path to separate CSS file (optional)",
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-5-20251122",
        help="Claude model to use for analysis",
    )
    args = parser.parse_args()

    from scraper.analyzer import analyze_design

    # Determine if input is URL or local file
    input_path = Path(args.input)
    if input_path.exists():
        print(f"Reading local file: {input_path}")
        html = input_path.read_text()
        css = ""
        if args.css:
            css = Path(args.css).read_text()
    else:
        from scraper.fetcher import fetch_website
        print(f"Fetching {args.input}...")
        html, css, _ = fetch_website(args.input)

    # Create output directory
    output_dir = Path(args.output) / args.name
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Analyzing design with LLM ({args.model})...")
    design_data, design_content = analyze_design(html, css, args.name)

    # Save DESIGN.md
    design_path = output_dir / "DESIGN.md"
    design_path.write_text(design_content)
    print(f"Created {design_path}")

    # Save extracted data as JSON (for debugging/reference)
    import json
    from dataclasses import asdict
    json_path = output_dir / "design_data.json"
    json_path.write_text(json.dumps(asdict(design_data), indent=2))

    print(f"Done! Output saved to {output_dir}/")
    print(f"\nPreview:\n{'='*50}\n{design_content[:500]}...\n{'='*50}")


if __name__ == "__main__":
    main()
