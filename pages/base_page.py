# -*- coding: utf-8 -*-
"""BasePage – common methods shared by all Page Object Models."""
import allure
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page, config: dict):
        self.page = page
        self.config = config
        self.base_url = config["base_url"]
        self.timeout = config["timeouts"]["element"]

    def navigate(self, path: str):
        with allure.step(f"Navigate to {path}"):
            self.page.goto(f"{self.base_url}{path}")
            self.page.wait_for_load_state("networkidle", timeout=self.config["timeouts"]["network_idle"])

    def wait_for_heading(self, text: str):
        with allure.step(f"Wait for heading: {text}"):
            locator = self.page.locator(f"h1:has-text('{text}'), h2:has-text('{text}')")
            locator.first.wait_for(timeout=self.timeout)
            return locator.first

    def fill(self, selector: str, value: str, label: str = ""):
        with allure.step(f"Fill '{label or selector}' with '{value}'"):
            self.page.locator(selector).first.fill(value)

    def click(self, selector: str, label: str = ""):
        with allure.step(f"Click '{label or selector}'"):
            self.page.locator(selector).first.click()

    def click_button(self, text: str):
        with allure.step(f"Click button: {text}"):
            self.page.locator(f"button:has-text('{text}'), a:has-text('{text}')").first.click()

    def search(self, selector: str, term: str):
        with allure.step(f"Search for '{term}'"):
            self.page.locator(selector).first.fill(term)
            self.page.wait_for_load_state("networkidle", timeout=self.config["timeouts"]["network_idle"])

    def get_table_row_count(self) -> int:
        with allure.step("Count table rows"):
            return self.page.locator("table tbody tr").count()

    def get_toast_message(self) -> str:
        """Get the text of a toast/snackbar notification."""
        try:
            toast = self.page.locator("[data-sonner-toast], .toast, [role='status']")
            toast.first.wait_for(timeout=5000)
            return toast.first.inner_text().strip()
        except Exception:
            return ""

    def is_page_error(self) -> bool:
        """Check if the page shows an error boundary."""
        error_selectors = [
            "div#__next_error__",
            "[data-nextjs-error]",
            "h1:text-is('Application error: a client-side exception has occurred')",
            "h1:text-is('500')",
        ]
        for sel in error_selectors:
            if self.page.locator(sel).count() > 0:
                return True
        return False

    def current_url(self) -> str:
        return self.page.url

    def page_title(self) -> str:
        return self.page.title()

    def take_screenshot(self, name: str):
        with allure.step(f"Screenshot: {name}"):
            screenshot = self.page.screenshot(full_page=True)
            allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
