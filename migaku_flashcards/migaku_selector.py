import os
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright

load_dotenv()
script_dir = Path(__file__).parent
env_path = script_dir / ".env"
load_dotenv(dotenv_path=env_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # --- log in ---
    page.goto("https://study.migaku.com/login")
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill(USERNAME)
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password").fill(PASSWORD)
    page.get_by_role("button", name="Log in").click()
    page.wait_for_timeout(1000)

    # --- navigate to HSK 6 deck and open select menu ---
    page.goto("https://study.migaku.com/?selectLanguage=true")
    page.get_by_role("button", name="Mandarin flag Mandarin 10,173").click()
    page.get_by_role("link").nth(1).click()
    page.get_by_role("button", name="H HSK 6 8158 new 8558 cards").click()
    page.get_by_role("button", name="More actions").click()
    page.get_by_role("button", name="Select...").click()

    # --- infinite scroll until no more cards load ---
    previous_height = 0
    while True:
        page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        current_height = page.evaluate("document.body.scrollHeight")
        if current_height == previous_height:
            break
        previous_height = current_height

    # --- select every even‐indexed card (2,4,6,…) ---
    cards = page.locator("div.DynamicList__item")
    total = cards.count()
    for index in range(total):
        if (index + 1) % 2 == 0:
            cards.nth(index).locator(".UiCheckbox__input").click()

    # --- wait for your confirmation before finishing ---
    input("Press Enter to continue...")

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
