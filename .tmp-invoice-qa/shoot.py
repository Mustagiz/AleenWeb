import os
from playwright.sync_api import sync_playwright

BASE = "http://localhost:3002"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")
os.makedirs(OUT, exist_ok=True)

TEMPLATES = [
    "Atelier Royal Emerald",
    "Classic Champagne Gold",
    "Royal Velvet Sapphire",
    "Rose Gold & Dusty Plum",
    "Kashmiri Heritage Crimson",
    "Executive Monolith Slate",
    "Modern Minimalist Haute",
    "Compact POS Boutique Slip",
]
SLUG = {t: t.replace(" ", "-").replace("&", "and") for t in TEMPLATES}


def run(mode, tall=False):
    height = 2400 if tall else 1000
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": height})
        page.goto(BASE, wait_until="load", timeout=60000)
        page.wait_for_timeout(2500)
        try:
            page.get_by_role("button", name="Auto-Fill Demo Credentials").click(timeout=5000)
        except Exception as exc:
            print("autofill skip:", exc)
        page.get_by_role("button", name="Sign In").click(timeout=10000)
        page.wait_for_timeout(3500)

        page.evaluate("m => localStorage.setItem('themeMode', m)", mode)
        page.goto(BASE + "/settings?tab=invoice", wait_until="load", timeout=60000)
        page.reload(wait_until="load")
        page.wait_for_timeout(3500)

        label = page.locator("text=Default Print Template:").first
        label.scroll_into_view_if_needed()
        page.wait_for_timeout(800)

        if tall:
            grid = label.locator("xpath=following-sibling::div[1]")
            grid.screenshot(path=os.path.join(OUT, f"gallery-{mode}.png"))
            print("gallery shot", mode)
        else:
            for tmpl in TEMPLATES:
                page.get_by_text(tmpl, exact=True).first.click(timeout=6000)
                page.wait_for_timeout(900)
                el = page.locator("#printable-invoice").first
                el.scroll_into_view_if_needed()
                page.wait_for_timeout(300)
                page.screenshot(path=os.path.join(OUT, f"{mode}-{SLUG[tmpl]}.png"), clip=el.bounding_box())
                print(mode, "|", tmpl)
        browser.close()


run("light", tall=True)
run("dark", tall=True)
run("light")
run("dark")
print("done", OUT)
