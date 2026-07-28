import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

# ============================================
# Validate arguments
# ============================================

if len(sys.argv) < 3:
    raise RuntimeError(
        "Usage: python scripts/tiktok_uploader.py <video_path> <caption>"
    )

VIDEO_FILE = Path(sys.argv[1])
CAPTION = sys.argv[2]

if not VIDEO_FILE.exists():
    raise FileNotFoundError(f"Video not found: {VIDEO_FILE}")

print(f"Using video: {VIDEO_FILE.name}")

# ============================================
# Paths
# ============================================

COOKIE_FILE = Path("app/auth/www_tiktok_com_cookies.json")

# ============================================
# Load cookies
# ============================================

with open(COOKIE_FILE, "r", encoding="utf-8") as f:
    raw_cookies = json.load(f)

cookies = []

same_site_map = {
    "no_restriction": "None",
    "lax": "Lax",
    "strict": "Strict",
    "unspecified": None,
}

for c in raw_cookies:
    cookie = {
        "name": c["name"],
        "value": c["value"],
        "domain": c["domain"],
        "path": c.get("path", "/"),
        "httpOnly": c.get("httpOnly", False),
        "secure": c.get("secure", False),
    }

    if "expirationDate" in c:
        cookie["expires"] = int(c["expirationDate"])

    same_site = same_site_map.get(c.get("sameSite", "").lower())

    if same_site is not None:
        cookie["sameSite"] = same_site

    cookies.append(cookie)

print(f"Loaded {len(cookies)} cookies.")

# ============================================
# Playwright
# ============================================

with sync_playwright() as p:
    browser = p.chromium.launch(
        channel="chrome",
        headless=False,
    )

    context = browser.new_context()

    print("Importing cookies...")
    context.add_cookies(cookies)

    page = context.new_page()

    print("Opening TikTok Studio...")

    page.goto(
        "https://www.tiktok.com/tiktokstudio/upload",
        wait_until="domcontentloaded",
        timeout=60000,
    )

    page.wait_for_timeout(5000)

    print("Current URL:", page.url)

    upload_button = page.locator(
        '[data-e2e="select_video_button"]'
    )

    print(f"Upload buttons found: {upload_button.count()}")

    if upload_button.count() == 0:
        browser.close()
        raise RuntimeError("Could not find the Select Video button.")

    print("Waiting for file chooser...")

    with page.expect_file_chooser() as fc_info:
        upload_button.first.click()

    file_chooser = fc_info.value

    print(f"Uploading: {VIDEO_FILE.name}")

    file_chooser.set_files(str(VIDEO_FILE.resolve()))

    print("✅ Video selected!")

    # Wait while TikTok uploads the video
    page.wait_for_timeout(30000)

    # -----------------------------
    # Automatic content checks
    # -----------------------------
    try:
        turn_on_button = page.get_by_role(
            "button",
            name="Turn on"
        )

        if turn_on_button.is_visible(timeout=5000):
            print("Found 'Automatic content checks' dialog.")
            turn_on_button.click()
            print("Clicked 'Turn on'.")
            page.wait_for_timeout(3000)

    except Exception:
        print("No 'Automatic content checks' dialog.")

    # -----------------------------
    # Tutorial popup
    # -----------------------------
    try:
        got_it_button = page.get_by_role(
            "button",
            name="Got it"
        )

        if got_it_button.is_visible(timeout=5000):
            print("Found tutorial popup.")
            got_it_button.click()
            print("Clicked 'Got it'.")
            page.wait_for_timeout(2000)

    except Exception:
        print("No tutorial popup.")

    # ============================================
    # Fill caption
    # ============================================

    caption = page.locator(
        '[data-e2e="caption_container"] [contenteditable="true"]'
    )

    caption.wait_for(timeout=10000)
    caption.click()

    try:
        caption.press("Control+A")
        caption.press("Backspace")
    except Exception:
        pass

    caption.type(
        CAPTION,
        delay=15,
    )

    print("✅ Caption filled.")

    # ============================================
    # Scroll to Post button
    # ============================================

    post_button = page.locator(
        '[data-e2e="post_video_button"]'
    )

    post_button.scroll_into_view_if_needed()

    page.wait_for_timeout(1000)

    print("✅ Scrolled to Post button.")

    # ============================================
    # Click Post
    # ============================================

    post_button.click()

    print("🚀 Post button clicked!")

    page.wait_for_timeout(10000)

    print("Upload process should now be running.")

    browser.close()