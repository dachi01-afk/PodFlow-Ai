import json
from pathlib import Path
from playwright.sync_api import sync_playwright


class TikTokUploader:
    def __init__(self):
        self.cookie_file = Path("app/auth/www_tiktok_com_cookies.json")

    def has_session(self) -> bool:
        return self.cookie_file.exists()

    def upload(self, video_path: str, caption_text: str):
        video_file = Path(video_path)

        if not video_file.exists():
            raise FileNotFoundError(f"Video not found: {video_file}")

        # ==========================
        # Load cookies
        # ==========================

        with open(self.cookie_file, "r", encoding="utf-8") as f:
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

            same_site = same_site_map.get(
                c.get("sameSite", "").lower()
            )

            if same_site is not None:
                cookie["sameSite"] = same_site

            cookies.append(cookie)

        print(f"Loaded {len(cookies)} cookies.")

        # ==========================
        # Playwright
        # ==========================

        with sync_playwright() as p:
            browser = p.chromium.launch(
                channel="chrome",
                headless=False,
            )

            context = browser.new_context()

            context.add_cookies(cookies)

            page = context.new_page()

            page.goto(
                "https://www.tiktok.com/tiktokstudio/upload",
                wait_until="domcontentloaded",
                timeout=60000,
            )

            page.wait_for_timeout(5000)

            upload_button = page.locator(
                '[data-e2e="select_video_button"]'
            )

            if upload_button.count() == 0:
                browser.close()
                raise RuntimeError(
                    "Could not find Select Video button."
                )

            with page.expect_file_chooser() as fc_info:
                upload_button.first.click()

            file_chooser = fc_info.value
            file_chooser.set_files(str(video_file.resolve()))

            print(f"Uploading {video_file.name}")

            page.wait_for_timeout(30000)

            # --------------------------
            # Automatic content checks
            # --------------------------

            try:
                turn_on_button = page.get_by_role(
                    "button",
                    name="Turn on"
                )

                if turn_on_button.is_visible(timeout=5000):
                    turn_on_button.click()
                    page.wait_for_timeout(3000)

            except Exception:
                pass

            # --------------------------
            # Tutorial popup
            # --------------------------

            try:
                got_it_button = page.get_by_role(
                    "button",
                    name="Got it"
                )

                if got_it_button.is_visible(timeout=5000):
                    got_it_button.click()
                    page.wait_for_timeout(2000)

            except Exception:
                pass

            # --------------------------
            # Caption
            # --------------------------

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
                caption_text,
                delay=15,
            )

            print("Caption filled.")

            # --------------------------
            # Post
            # --------------------------

            post_button = page.locator(
                '[data-e2e="post_video_button"]'
            )

            post_button.scroll_into_view_if_needed()

            page.wait_for_timeout(1000)

            post_button.click()

            print("Post button clicked.")

            page.wait_for_timeout(10000)

            browser.close()