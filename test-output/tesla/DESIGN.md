# 1. Visual Theme & Atmosphere

**Serif Industrialism & Digital Print**
This design system reimagines the typical tech aesthetic by rejecting the ubiquitous sans-serif in favor of a classical, high-contrast serif typography (Times New Roman). The visual philosophy is "Digital Editorial" — treating the web browser like a high-end printed magazine page. It strips away all decorative elements (gradients, rounded corners, drop shadows) to focus entirely on typography, grid, and negative space.

**Stark, Uncompromising, and Intellectual**
The atmosphere is cold, precise, and authoritative. By combining 0px border radius with classic serif fonts, the design communicates heritage and durability rather than fleeting trends. The high contrast between pure black backgrounds and white text in the hero section creates a dramatic, showroom-like environment where the content feels heavier and more significant.

**Whitespace as Structure**
The design relies heavily on massive amounts of vertical whitespace (whitespace) to create rhythm. There are no container lines separating sections; instead, breathing room defines the layout. The "density" is low — elements are sparse, forcing the user to slow down and absorb the information.

---

# 2. Color Palette & Roles

### Primary
- **Tesla Red** (`#e82127`): The signature action color (rgb 232, 33, 39). Used strictly for primary conversion buttons or critical alerts. It provides the only burst of saturation in the interface.
- **Obsidian** (`#171a20`): The primary text color on white backgrounds (rgb 23, 26, 32). It is not pure black, providing a softer, more premium reading experience on paper-white screens.

### Secondary & Accent
- **Concrete Grey** (`#f4f4f4`): The standard button background (rgb 244, 244, 244). A very light grey that sits slightly off-white to distinguish interactive elements from the page background.
- **Frost White** (`#ffffff`): The primary canvas color (rgb 255, 255, 255).

### Surface & Background
- **Vantablack** (`#000000`): The hero section background and footer background (rgb 0, 0, 0). Used to create dramatic "night mode" zones.
- **Off-White Card** (`#fafafa`): Used for card backgrounds to slightly differentiate from the main body (rgb 250, 250, 250).

### Neutrals & Text
- **Muted Graphite** (`#5c5e62`): Secondary text, footer text, and subheadings (rgb 92, 94, 98).
- **Frosted Overlay** (`rgba(255, 255, 255, 0.92)`): The header background to allow content scroll-through while maintaining legibility.

### Semantic
- **None defined**: The system relies on color temperature (Black/White/Red) rather than functional semantic colors (Green/Yellow) for this specific aesthetic.

---

# 3. Typography Rules

**Font Family:**
`"Times New Roman", Times, "Liberation Serif", "Noto Serif", serif`

**OpenType Features:**
Standard kerning. No ligatures enabled. All caps are achieved via CSS `text-transform: uppercase` combined with generous `letter-spacing`.

| Role | Size | Weight | Line Height | Letter Spacing | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero Title** | clamp(2.5rem, 6vw, 3.75rem) | 400 | 1.2 | -0.02em | Tight tracking for headline impact |
| **Logo / Wordmark** | 1.125rem (18px) | 400 | 1.5 | 0.2em | Uppercase, widely spaced |
| **Section Title** | 1.75rem (28px) | 400 | 1.2 | 0 | Serif display style |
| **Nav Item** | 0.875rem (14px) | 400 | 1.5 | 0 | Uppercase implied by size/style |
| **Button Label** | 0.875rem (14px) | 400 | 1.2 | 0.06em | Uppercase, widely spaced |
| **Body Text** | 1rem (16px) | 400 | 1.5 | 0 | Standard reading size |
| **Card Title** | 1.125rem (18px) | 400 | 1.2 | 0 | Slightly smaller than section title |
| **Footer Text** | 0.75rem (12px) | 400 | 1.5 | 0.04em | Uppercase for legal/disclaimers |

**Principles:**
*   **Weight Uniformity:** The system strictly uses `font-weight: 400` (Regular). There is no Bold (700). Hierarchy is established through size and case, not thickness.
*   **Text Transform:** Navigation and Buttons are exclusively UPPERCASE to maintain the "Industrial" aesthetic. Body copy remains Sentence case.
*   **Letter Spacing:** Wide spacing (0.06em+) is used for small UI elements (buttons, labels) to improve readability at small sizes. Negative spacing (-0.02em) is used only for massive headlines to tighten the visual bond between letters.

---

# 4. Component Stylings

### Buttons
*   **Primary Button (Standard):**
    *   `background`: #f4f4f4 (Concrete Grey)
    *   `color`: #171a20 (Obsidian)
    *   `padding`: 0.65rem 2.5rem (approx 10px vertical, 40px horizontal)
    *   `border-radius`: 0px (Strictly rectangular)
    *   `text-transform`: Uppercase
    *   `letter-spacing`: 0.06em
    *   `transition`: background 0.2s ease
    *   **Hover:** `background` becomes #e2e2e2 (darker grey)
*   **Primary Button (Inverse):**
    *   `background`: rgba(23, 26, 32, 0.85)
    *   `color`: #fff
    *   **Hover:** Opacity increases to 1.0
*   **Primary Button (Accent):**
    *   `background`: #e82127 (Tesla Red)
    *   `color`: #fff
    *   **Hover:** `filter: brightness(1.08)` (slight brighten)

### Cards & Containers
*   **Background:** #fafafa (Off-White)
*   **Border:** 1px solid rgba(0, 0, 0, 0.08) (Extremely subtle grey stroke)
*   **Radius:** 0px
*   **Padding:** 1.5rem (24px)
*   **Layout:** Vertical stack (Title -> Description)

### Inputs (Implied)
*   **Background:** #ffffff
*   **Border:** 1px solid rgba(0, 0, 0, 0.08)
*   **Radius:** 0px

### Navigation (Sticky Header)
*   **Position:** Fixed Top, Z-index 100
*   **Height:** Implicitly ~60px based on padding
*   **Background:** rgba(255, 255, 255, 0.92) with `backdrop-filter: blur(8px)`
*   **Border Bottom:** 1px solid rgba(0, 0, 0, 0.06)
*   **Layout:** Flexbox, Space-between

### Image Treatment
*   **Hero Handling:** Full viewport height (`min-height: 100vh`). Linear gradient overlay used to ensure text legibility (Dark to Darker).
*   **Lazy Loading:** Not explicitly defined in CSS, but implies heavy assets.

---

# 5. Layout Principles

**Spacing System:**
*   **Base Unit:** 16px (1rem)
*   **Common Values:**
    *   `0.5rem` (8px): Small gaps (Logo text)
    *   `1.5rem` (24px): Standard padding (Cards, Hero Horizontal)
    *   `2rem` (32px): Section vertical spacing
    *   `4rem` (64px): Large section padding
    *   `6rem` (96px): Hero top/bottom padding

**Grid & Container:**
*   **Max Width:** 72rem (1152px)
*   **Grid Pattern:** `grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr))`
    *   This creates a responsive grid that fits as many 14rem columns as possible without wrapping.

**Whitespace Philosophy:**
Space is not empty; it is the container for the content. The design avoids crowding. If an element feels crowded, increase padding to `4rem`. Margins between sections should be `2rem` or greater.

**Border Radius Scale:**
| Value | Context |
| :--- | :--- |
| **0px** | 100% of UI elements (Buttons, Cards, Inputs, Containers) |

---

# 6. Depth & Elevation

**Elevation Levels:**
| Level | Treatment | Use |
| :--- | :--- | :--- |
| **Level 0** | 1px solid rgba(0,0,0,0.08) border | Cards, Inputs |
| **Level 1** | Box-shadow 0 1px 3px rgba(0,0,0,0.12) | Primary Buttons (Active) |
| **Level 2** | Backdrop-filter blur(8px) + Border | Sticky Navigation |

**Shadow Philosophy:**
Shadows are used exclusively for interactive feedback (buttons) to indicate "pressability." They are never used for decorative depth. The navigation uses glassmorphism (blur) instead of a solid block color to feel lighter.

**Decorative Depth:**
Gradients are used purely for text contrast (Hero section gradient) rather than surface texture. No skeuomorphism or texture is present.

---

# 7. Do's and Don'ts

**Do:**
1.  **Do** maintain 0px border radius on all geometric shapes. Sharp corners are mandatory.
2.  **Do** use Times New Roman (or serif fallback) for all typography.
3.  **Do** use `font-weight: 400` (Regular) for everything. Do not use bold.
4.  **Do** uppercase all button labels and small labels with `0.06em` letter spacing.
5.  **Do** use `rgba` backgrounds for overlays to maintain visual depth.
6.  **Do** keep text contrast high (Black on White, White on Black).
7.  **Do** center align Hero content.
8.  **Do** use the specific "Tesla Red" only for the primary call-to-action.
9.  **Do** apply `backdrop-filter: blur(8px)` to the sticky header.
10. **Do** allow the grid to flow naturally using `auto-fit`.

**Don't:**
1.  **Don't** round corners (e.g., `border-radius: 4px` or `50%` is forbidden).
2.  **Don't** use Sans-Serif fonts (Arial, Roboto, Inter) unless absolutely necessary for technical data.
3.  **Don't** use drop shadows on cards; use only borders.
4.  **Don't** place heavy font weights (Bold/Black) on headings.
5.  **Don't** use gradients on buttons (flat color only).
6.  **Don't** use blue as a link color; use standard text color.
7.  **Don't** clutter the footer; keep it a single dark strip with centered text.
8.  **Don't** use `border: none` on cards; the 1px border is structural.
9.  **Don't** mix uppercase headers with lowercase body text headers without clear size hierarchy.
10. **Don't** reduce whitespace below the standard 1.5rem rhythm.

---

# 8. Responsive Behavior

**Breakpoints:**
| Name | Width | Key Changes |
| :--- | :--- | :--- |
| **Mobile** | < 768px | Flex direction switches to column. Grid becomes 1 column. |
| **Tablet** | 768px - 1024px | Grid becomes 2 columns. |
| **Desktop** | > 1024px | Grid becomes 3+ columns. Full horizontal navigation visible. |

**Touch Targets:**
*   **Minimum Button Height:** 44px (implied by padding `0.65rem`).
*   **Padding:** Generous horizontal padding (`2.5rem`) ensures fingers have room to tap.

**Collapsing Strategy:**
*   **Navigation:** On mobile (simulated via flex-wrap), links should stack or move to a hamburger menu (not explicitly coded in this demo, but standard behavior for this layout).
*   **Grid:** The `repeat(auto-fit, minmax(14rem, 1fr))` automatically handles collapsing. If the screen is narrower than 14rem per card, they stack vertically.

**Image Behavior:**
*   **Hero:** `min-height: 100vh` ensures the hero always covers the full screen regardless of device orientation. Text size uses `clamp()` to scale smoothly between mobile and desktop.

---

# 9. Agent Prompt Guide

**Quick Color Reference:**
*   `--text`: #171a20
*   `--text-muted`: #5c5e62
*   `--bg`: #ffffff
*   `--accent`: #e82127
*   `--btn-bg`: #f4f4f4

**Example Component Prompts:**
1.  "Create a sticky header with a glassmorphism effect (rgba 255, 255, 255, 0.92). Place a serif logo 'TESLA' on the left and 3 uppercase text links on the right."
2.  "Design a 'Primary Action Button' using Times New Roman. It must be rectangular (0px radius), light grey background (#f4f4f4), dark text, uppercase, and have tight padding."
3.  "Generate a hero section with a black-to-dark-grey gradient background. Center a large Serif H1 title (3.75rem) and two buttons below it: one dark transparent, one light grey."
4.  "Create a 3-column grid of cards. Each card should have a 1px subtle grey border, #fafafa background, and no border radius."
5.  "Design a footer strip with pure black background (#000) and centered small grey text (12px)."

**Iteration Guide:**
*   **If the AI uses Sans-Serif:** Explicitly state "FORCE serif font-family Times New Roman."
*   **If buttons are round:** Remind the agent "NO border-radius allowed. Corners must be sharp."
*   **If it looks too 'techy':** Ask to "Increase whitespace" and "Remove all drop shadows except on buttons."
*   **Focus First:** Always establish the typography (Serif) and the color contrast (Black/White) before building components.