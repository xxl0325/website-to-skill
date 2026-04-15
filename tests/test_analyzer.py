"""Tests for design analyzer."""

from scraper.analyzer import extract_colors, extract_fonts, analyze_design


def test_extract_colors():
    """Test color extraction from CSS."""
    css = """
        :root {
            --primary-color: #3E6AE1;
            --background: #FFFFFF;
        }
    """
    colors = extract_colors(css)
    assert colors.get("primary") == "#3E6AE1" or "#FFFFFF" in colors.values()


def test_extract_fonts():
    """Test font extraction from CSS."""
    css = """
        body {
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            font-weight: 400;
        }
    """
    fonts = extract_fonts(css)
    assert "Inter" in fonts.get("family", "")


def test_analyze_design():
    """Test full design analysis."""
    html = '<button class="btn-primary">Click</button>'
    css = """
        .btn-primary {
            background-color: #3E6AE1;
            border-radius: 4px;
        }
    """
    design = analyze_design(html, css)
    assert design.colors or design.buttons
