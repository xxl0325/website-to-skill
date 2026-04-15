"""Fetch website HTML, CSS, and screenshot using Playwright."""

from pathlib import Path
from playwright.sync_api import sync_playwright


import random
import time


# Realistic User-Agent strings to avoid detection
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15",
]


def fetch_with_httpx(url: str) -> tuple[str, str] | None:
    """
    Try to fetch website using httpx with TLS fingerprinting bypass.
    Returns (html, css) or None if failed.
    """
    try:
        import httpx

        # Use a real browser's TLS fingerprint
        headers = {
            "User-Agent": USER_AGENTS[0],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }

        # Add random delay to appear more human
        time.sleep(random.uniform(1.0, 3.0))

        response = httpx.get(
            url,
            headers=headers,
            timeout=30.0,
            follow_redirects=True,
        )

        if response.status_code != 200:
            return None

        html = response.text

        # Basic check - if HTML is too short or looks like error, skip
        if len(html) < 1000:
            return None
        if "Access Denied" in html or "403" in html or "captcha" in html.lower():
            return None

        # Extract CSS from inline styles
        css = ""
        import re
        style_matches = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)
        for style in style_matches:
            css += style + "\n"

        return html, css

    except Exception as e:
        print(f"httpx fetch failed: {e}")
        return None


def check_error_page(html: str, url: str) -> None:
    """Check if the fetched HTML is an error page and raise an exception if so."""
    error_indicators = [
        ("Access Denied", "CDN Access Denied"),
        ("403 Forbidden", "403 Forbidden"),
        ("404 Not Found", "404 Not Found"),
        ("502 Bad Gateway", "502 Bad Gateway"),
        ("503 Service Unavailable", "503 Service Unavailable"),
        ("Akamai", "Akamai CDN Error"),
        ("Cloudflare", "Cloudflare CDN Error"),
        ("<title>Just a moment</title>", "Cloudflare Challenge"),
        ("Enable JavaScript and cookies", "Bot Detection Page"),
        ("captcha", "Captcha Challenge"),
        ("edge_suite", "Akamai EdgeSuite"),
        ("Reference #", "Akamai Reference ID"),
    ]

    for indicator, error_type in error_indicators:
        if indicator.lower() in html.lower():
            raise RuntimeError(
                f"Website returned an error page: {error_type}\n"
                f"URL: {url}\n"
                f"This usually means the site is blocking automated requests.\n"
                f"Try using a different IP, adding delays, or accessing via API."
            )


def fetch_website(url: str, screenshot_path: str = None) -> tuple[str, str, bytes]:
    """
    Fetch website HTML, CSS, and optionally take a screenshot.
    Tries httpx first for better compatibility, falls back to Playwright.

    Args:
        url: Website URL to fetch
        screenshot_path: Optional path to save screenshot

    Returns:
        Tuple of (html_content, css_content, screenshot_bytes)
    """
    # Try httpx first - lighter weight and sometimes bypasses detection
    result = fetch_with_httpx(url)
    if result:
        html, css = result
        print(f"Successfully fetched {url} using httpx")
        check_error_page(html, url)
        return html, css, b""

    # Fall back to Playwright
    print("Falling back to Playwright for browser-based fetch...")
    html = ""
    css = ""
    screenshot = b""

    with sync_playwright() as p:
        # Launch browser with anti-detection settings
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-web-security",
            ]
        )

        # Create context with realistic fingerprint
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=USER_AGENTS[0],  # Use a real Mac Chrome UA
            locale="en-US",
            timezone_id="America/Los_Angeles",
            # Simulate a real user with color scheme
            color_scheme="light",
            # Add extra HTTP headers to appear more legitimate
            extra_http_headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0",
            },
        )

        # Add stealth scripts to avoid detection
        page = context.new_page()

        # Inject JavaScript to hide automation signatures
        page.add_init_script("""
            // Hide webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // Hide automation-related properties
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            // Mock languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });

            // Mock permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );

            // Mock hardware concurrency
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => 8
            });

            // Mock device memory
            Object.defineProperty(navigator, 'deviceMemory', {
                get: () => 8
            });

            // Mock touch points
            Object.defineProperty(navigator, 'maxTouchPoints', {
                get: () => 5
            });
        """)

        try:
            # Add random delay before navigation to appear more human
            import random
            page.wait_for_timeout(random.randint(500, 1500))

            # Navigate with realistic timing - try multiple wait strategies
            page.goto(url, wait_until="domcontentloaded", timeout=30000)

            # Wait for network to be idle (but with shorter timeout to avoid hanging)
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except:
                # If networkidle times out, continue anyway
                pass

            # Small delay to allow any lazy-loaded content
            page.wait_for_timeout(random.randint(1000, 2000))

            html = page.content()

            # Check if we got an error page
            check_error_page(html, url)

            # Extract all stylesheets and inline styles
            css = page.evaluate("""
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
            """)

            # Take screenshot if requested
            if screenshot_path:
                screenshot = page.screenshot(full_page=True)

        finally:
            context.close()
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
        # Launch with anti-detection
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ]
        )

        for name, viewport in viewports.items():
            # Create context with realistic fingerprint
            context = browser.new_context(
                viewport=viewport,
                user_agent=USER_AGENTS[0],
                locale="en-US",
                timezone_id="America/Los_Angeles",
            )

            page = context.new_page()

            # Inject stealth scripts
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(1000)

                html = page.content()

                # Check if we got an error page
                check_error_page(html, url)

                results[name] = {
                    "html": html,
                    "css": page.evaluate("() => document.querySelectorAll('style')[0]?.textContent || ''"),
                    "screenshot": page.screenshot(full_page=True),
                }

                # Save individual files
                output_path = Path(output_dir)
                (output_path / f"{name}.html").write_text(results[name]["html"])
                (output_path / f"{name}.css").write_text(results[name]["css"])
                (output_path / f"{name}.png").write_bytes(results[name]["screenshot"])

            finally:
                context.close()
                page.close()

        browser.close()

    return results
