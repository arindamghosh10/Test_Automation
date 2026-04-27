# -*- coding: utf-8 -*-
"""LoginPage – handles sign-in flow."""
import allure
from pages.base_page import BasePage


class LoginPage(BasePage):
    # Locators
    LOGIN_LINK     = 'a:has-text("Securely Login With Email")'
    EMAIL_INPUT    = 'input[type="email"], input[name="email"], input[name="username"]'
    PASSWORD_INPUT = 'input[type="password"]'
    SUBMIT_BTN     = 'button[type="submit"], button:has-text("Continue"), button:has-text("Sign in")'
    ERROR_MSG      = '[class*="error"], [role="alert"], p.text-red, p.text-destructive'

    def go_to_login(self):
        with allure.step("Open sign-in page"):
            self.navigate("/sign-in?redirect=%2Fcompany-admin%2Fdashboard")

    def click_secure_login(self):
        with allure.step("Click 'Securely Login With Email'"):
            self.page.locator(self.LOGIN_LINK).click()
            self.page.wait_for_load_state("networkidle")

    def enter_email(self, email: str):
        with allure.step(f"Enter email: {email}"):
            self.page.locator(self.EMAIL_INPUT).first.fill(email)

    def enter_password(self, password: str):
        with allure.step("Enter password"):
            self.page.locator(self.PASSWORD_INPUT).first.fill(password)

    def click_submit(self):
        with allure.step("Click Submit / Continue"):
            self.page.locator(self.SUBMIT_BTN).first.click()

    def login(self, email: str, password: str, expected_url_pattern: str = "**/company-admin/dashboard"):
        """Full login flow."""
        self.go_to_login()
        self.click_secure_login()
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()
        self.page.wait_for_url(expected_url_pattern, timeout=self.config["timeouts"]["page_load"])
        self.page.wait_for_load_state("networkidle")

    def get_error_message(self) -> str:
        with allure.step("Get error message"):
            try:
                el = self.page.locator(self.ERROR_MSG).first
                el.wait_for(timeout=5000)
                return el.inner_text().strip()
            except Exception:
                return ""

    def is_on_login_page(self) -> bool:
        return "sign-in" in self.page.url or "login" in self.page.url
