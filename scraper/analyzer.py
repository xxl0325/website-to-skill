"""Analyze website HTML/CSS/Screenshot using LLM to generate detailed DESIGN.md."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DesignData:
    """Complete design system data for a brand."""
    brand_name: str = ""
    visual_identity: str = ""
    colors: dict = field(default_factory=dict)
    color_usage: dict = field(default_factory=dict)
    fonts: dict = field(default_factory=dict)
    typography_hierarchy: list = field(default_factory=list)
    components: dict = field(default_factory=dict)
    layout: dict = field(default_factory=dict)
    spacing: dict = field(default_factory=dict)
    depth_elevation: dict = field(default_factory=dict)
    responsive: dict = field(default_factory=list)
    dos_donts: dict = field(default_factory=dict)
    agent_prompts: dict = field(default_factory=dict)


ANALYZE_PROMPT = """
You are a design systems expert analyzing a website to create comprehensive documentation.

Your task: Analyze the provided HTML/CSS and generate a complete DESIGN.md document that could be given to an AI to regenerate this UI.

The output MUST have exactly these 9 sections:

# 1. Visual Theme & Atmosphere

Write 2-3 paragraphs describing:
- Overall visual style and design philosophy
- Emotional tone and brand personality
- Photography/illustration style
- UI density and whitespace usage
- What makes this design distinctive

Example tone: "Tesla's website is an exercise in radical subtraction — a digital showroom where the product is everything and the interface is almost nothing..."

# 2. Color Palette & Roles

For EACH color, provide:
- Descriptive name (e.g., "Electric Blue", "Carbon Dark")
- Hex value
- RGB values in format: (rgb R, G, B)
- Specific usage context

Organize into groups:
- **Primary**: Main brand/CTA colors
- **Secondary & Accent**: Supporting colors
- **Surface & Background**: Background colors including transparent values
- **Neutrals & Text**: Text hierarchy colors
- **Semantic**: Status colors if any

Format example:
- **Electric Blue** (`#3E6AE1`): Primary CTA button background — a confident, mid-saturation blue (rgb 62, 106, 225) used exclusively for "Order Now" buttons

# 3. Typography Rules

Include:
- **Font Family**: Complete font stack with fallbacks
- Any OpenType features or special variants
- Typography hierarchy TABLE with columns:
  | Role | Size | Weight | Line Height | Letter Spacing | Notes |

Roles should include: Hero Title, Product Name, Nav Item, Body Text, Button Label, Sub-link, etc.

Add **Principles** section covering:
- Weight usage patterns (e.g., "Only 400-500, no bold")
- Text transform conventions
- Letter spacing philosophy
- Display vs Text variant usage

# 4. Component Stylings

Detail EVERY interactive element with exact CSS values:

**Buttons** — break down by type:
- Primary CTA: bg, text color, fontSize, fontWeight, padding, borderRadius, minHeight, width, border, transition timing, hover state
- Secondary CTA: same details
- Nav Button / Text Link: same details

**Cards & Containers**:
- Background, border, shadow, content layout, hover behavior

**Inputs & Forms**:
- Background, text color, placeholder color, border treatment

**Navigation**:
- Desktop layout, dropdown behavior, mobile collapse pattern, background treatments

**Image Treatment**:
- Hero image handling, lazy loading, carousel behavior

For each component, include usage notes like "Used for: 'Order Now' calls to action"

# 5. Layout Principles

**Spacing System**:
- Base unit (e.g., 8px)
- Common values with rem equivalents
- Button padding, section padding, card gap

**Grid & Container**:
- Max width values
- Layout patterns (e.g., "3-column grid", "2-up horizontal")

**Whitespace Philosophy**:
- 1-2 paragraphs on how space creates luxury/rhythm

**Border Radius Scale** — TABLE:
| Value | Context |
|-------|---------|
| 0px | Most elements |
| 4px | Buttons |
| 12px | Large cards |

# 6. Depth & Elevation

Create elevation TABLE:
| Level | Treatment | Use |
|-------|-----------|-----|
| Level 0 | No shadow, no border | Default state |
| Level 1 | Frosted glass | Navigation on scroll |

**Shadow Philosophy**:
1-2 paragraphs on approach to depth (shadows vs alternatives)

**Decorative Depth**:
Gradients, glows, atmospheric effects — or note their absence

# 7. Do's and Don'ts

**Do** (8-10 items):
- Actionable rules with specific values
- Reference exact colors by name
- Include interaction timing rules

**Don't** (8-10 items):
- What breaks the design system
- What contradicts the visual identity
- Common mistakes to avoid

# 8. Responsive Behavior

**Breakpoints** — TABLE:
| Name | Width | Key Changes |
|------|-------|-------------|
| Mobile | <768px | Single-column, hamburger nav |
| Tablet | 768-1024px | 2-column layout |
| Desktop | 1024-1440px | Full horizontal nav |

**Touch Targets**:
- Minimum sizes for buttons, nav items

**Collapsing Strategy**:
- How navigation collapses
- How layouts reflow
- How spacing adapts

**Image Behavior**:
- Responsive image handling across breakpoints

# 9. Agent Prompt Guide

**Quick Color Reference**:
- Compact list mapping color names to hex values

**Example Component Prompts** (5-8 examples):
Write natural language prompts an AI would understand:
- "Create a hero section with full-viewport background image, centered title in Universal Sans Display at 40px weight 500..."
- "Design a navigation bar with spaced-letter wordmark on the left, five text buttons (14px, weight 500)..."

**Iteration Guide** (3-5 tips):
- How to refine generated output
- What to focus on first
- How to communicate desired "feel"

---

WRITING STYLE:
- Write in ENGLISH
- Use specific values: `4px` not "small", `#3E6AE1` not "blue"
- Give colors meaningful names based on usage
- Describe components with complete CSS properties
- Sound like a professional design system document
- Use descriptive prose for Visual Theme and philosophy sections
- Use technical precision for component specifications

---

Here is the website content:

HTML:
{html_content}

CSS:
{css_content}

Generate the complete DESIGN.md document:
"""


def analyze_design(html: str, css: str, brand_name: str = "") -> tuple[DesignData, str]:
    """
    Analyze website HTML/CSS using LLM to generate detailed design documentation.

    Args:
        html: Website HTML content
        css: Website CSS content
        brand_name: Brand name for the design

    Returns:
        Tuple of (DesignData, full_design_content_string)
    """
    import os
    from anthropic import Anthropic

    # Use environment variables for API configuration
    api_key = os.environ.get("ANTHROPIC_AUTH_TOKEN")
    base_url = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-0")

    # For DashScope/Alibaba proxy, use auth_token header
    client = Anthropic(
        base_url=base_url,
        default_headers={
            "Authorization": f"Bearer {api_key}",
        }
    )

    prompt = ANALYZE_PROMPT.format(
        html_content=html[:15000],  # Truncate to avoid token limits
        css_content=css[:15000]
    )

    response = client.messages.create(
        model=model,
        max_tokens=8000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract text from response (handle thinking models)
    design_content = ""
    for block in response.content:
        if hasattr(block, 'text'):
            design_content += block.text
        elif hasattr(block, 'type') and block.type == 'text':
            design_content += block.text

    # Create minimal DesignData for programmatic access
    data = DesignData()
    data.brand_name = brand_name or "Unknown"

    return data, design_content