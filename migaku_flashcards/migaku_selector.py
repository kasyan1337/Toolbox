import os
import time
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

    # log in
    page.goto("https://study.migaku.com/login")
    page.get_by_role("textbox", name="Email").fill(USERNAME)
    page.get_by_role("textbox", name="Password").fill(PASSWORD)
    page.get_by_role("button", name="Log in").click()
    page.wait_for_timeout(2000)

    # navigate to HSK-6 deck and select all
    page.goto("https://study.migaku.com/?selectLanguage=true")
    page.get_by_role("button", name="Mandarin flag Mandarin 10,173").click()
    page.get_by_role("link").nth(1).click()
    page.get_by_role("button", name="H HSK 6 8158 new 8558 cards").click()
    page.get_by_role("button", name="More actions").click()
    page.get_by_role("button", name="Select...").click()
    page.get_by_role("button", name="Select All").click()
    page.wait_for_timeout(1000)
    time.sleep(30)

    # scroll list until fully loaded
    page.evaluate("""
      async () => {
        const items = document.querySelectorAll('div.DynamicList__item');
        if (items.length === 0) return;
        const list = items[0].parentElement;
        let lastHeight = 0;
        while (true) {
          const height = list.scrollHeight;
          if (height === lastHeight) break;
          lastHeight = height;
          list.scrollTo(0, height);
          await new Promise(resolve => setTimeout(resolve, 500));
        }
      }
    """)

    # deselect all duplicate checkboxes (keep only first of each group)
    page.evaluate("""
      () => {
        const items = Array.from(document.querySelectorAll('div.DynamicList__item'));
        const groups = items.reduce((m, el) => {
          const text = el.innerText.trim();
          (m[text] = m[text] || []).push(el);
          return m;
        }, {});
        Object.values(groups).forEach(group => {
          if (group.length > 1) {
            group.slice(1).forEach(el => {
              const cb = el.querySelector('[role="checkbox"]');
              if (cb) cb.click();
            });
          }
        });
      }
    """)

    input("Press Enter to finish…")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)