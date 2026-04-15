"""Fetch website HTML, CSS, and screenshot using Playwright."""

from pathlib import Path
from playwright.sync_api import sync_playwright


def fetch_website(url: str, screenshot_path: str = None) -> tuple[str, str, bytes]:
    """
    Fetch website HTML, CSS, and optionally take a screenshot.

    Args:
        url: Website URL to fetch
        screenshot_path: Optional path to save screenshot

    Returns:
        Tuple of (html_content, css_content, screenshot_bytes)
    """
    html = ""
    css = ""
    screenshot = b""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url, wait_until="networkidle")
            html = page.content()

            # Extract all stylesheets and inline styles
            css = page.evaluate('''
                () => {
                    let allCss = '';

                    // Get inline stylesheets
                    document.querySelectorAll('style').forEach(style => {
                        allCss += style.textContent + '\\n';
                    });

                    // Get linked stylesheets
                    document.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
                        if (link.sheet) {
                            try {
                                allCss += link.sheet.cssText + '\\n';
                            } catch (e) {
                                // Cross-origin stylesheet
                            }
                        }
                    });

                    // Get inline styles
                    document.querySelectorAll('[style]').forEach(el => {
                        allCss += el.tagName.toLowerCase() + ' { ' + el.getAttribute('style') + ' }\\n';
                    });

                    return allCss;
                }
            ''')

            # Take screenshot if requested
            if screenshot_path:
                screenshot = page.screenshot(full_page=True)
                Path(screenshot_path).write_bytes(screenshot)

        finally:
            browser.close()

    return html, css, screenshot


def fetch_with_multiple_viewports(url: str, output_dir: str) -> dict:
    """
    Fetch website with multiple viewport sizes for responsive analysis.

    Args:
        url: Website URL
        output_dir: Directory to save outputs

    Returns:
        Dict with desktop/mobile html, css, screenshots
    """
    viewports = {
        "desktop": {"width": 1440, "height": 900},
        "tablet": {"width": 1024, "height": 768},
        "mobile": {"width": 390, "height": 844},
    }

    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for name, viewport in viewports.items():
            page = browser.new_page()
            page.set_viewport_size(viewport)

            try:
                page.goto(url, wait_until="networkidle")

                results[name] = {
                    "html": page.content(),
                    "css": page.evaluate("() => document.querySelectorAll('style')[0]?.textContent || ''"),
                    "screenshot": page.screenshot(full_page=True),
                }

                # Save individual files
                output_path = Path(output_dir)
                (output_path / f"{name}.html").write_text(results[name]["html"])
                (output_path / f"{name}.css").write_text(results[name]["css"])
                (output_path / f"{name}.png").write_bytes(results[name]["screenshot"])

            finally:
                page.close()

        browser.close()

    return results
