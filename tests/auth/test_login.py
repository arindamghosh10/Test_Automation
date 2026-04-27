# -*- coding: utf-8 -*-
"""
tests/auth/test_login.py
Auth tests: valid login, invalid credentials, logout, session.
"""
import pytest
import allure
from pages.login_page import LoginPage


@allure.suite("Authentication")
@allure.feature("Login")
class TestLogin:

    @allure.title("Valid login as Company Admin")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.auth
    def test_valid_login_company_admin(self, page, config):
        login = LoginPage(page, config)
        user = config["users"]["company_admin"]

        login.login(user["email"], user["password"])

        assert "/company-admin/dashboard" in page.url, \
            f"Expected dashboard URL, got: {page.url}"
        assert not login.is_on_login_page(), "Should not be on login page after valid login"
        login.take_screenshot("valid_login_success")

    @allure.title("Login with wrong password")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.auth
    def test_invalid_password(self, page, config):
        login = LoginPage(page, config)
        user = config["users"]["company_admin"]

        login.go_to_login()
        login.click_secure_login()
        login.enter_email(user["email"])
        login.enter_password("WrongPassword999!")
        login.click_submit()

        # Should stay on login page or show error
        import time; time.sleep(3)
        assert login.is_on_login_page() or login.get_error_message() != "", \
            "Expected error or redirect back to login with wrong password"
        login.take_screenshot("invalid_password_result")

    @allure.title("Login with empty email and password")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.auth
    def test_empty_credentials(self, page, config):
        login = LoginPage(page, config)

        login.go_to_login()
        login.click_secure_login()
        login.enter_email("")
        login.enter_password("")
        login.click_submit()

        import time; time.sleep(2)
        assert login.is_on_login_page(), "Should remain on login page with empty credentials"
        login.take_screenshot("empty_credentials_result")

    @allure.title("Login with invalid email format")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.auth
    def test_invalid_email_format(self, page, config):
        login = LoginPage(page, config)

        login.go_to_login()
        login.click_secure_login()
        login.enter_email("not-an-email")
        login.enter_password("SomePassword123!")
        login.click_submit()

        import time; time.sleep(2)
        assert login.is_on_login_page(), "Should stay on login with invalid email format"
        login.take_screenshot("invalid_email_format")

    @allure.title("Logout from dashboard")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.auth
    def test_logout(self, logged_in_page, config):
        page = logged_in_page

        # Click user avatar to open dropdown
        page.locator("button:has-text('M'), button[class*='rounded-full']").first.click()
        import time; time.sleep(1)

        # Click Logout
        page.locator("button:has-text('Logout'), a:has-text('Logout')").first.click()
        page.wait_for_load_state("networkidle")

        assert "sign-in" in page.url or "login" in page.url, \
            f"Expected to land on login page after logout, got: {page.url}"
        login = LoginPage(page, config)
        login.take_screenshot("after_logout")

    @allure.title("Session persists after page refresh")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.auth
    def test_session_persists_on_refresh(self, logged_in_page, config):
        page = logged_in_page
        page.reload()
        page.wait_for_load_state("networkidle")

        assert "/company-admin/dashboard" in page.url, \
            f"Session should persist after refresh, got: {page.url}"
        login = LoginPage(page, config)
        login.take_screenshot("session_after_refresh")

    @allure.title("Unauthenticated access redirects to login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.auth
    def test_unauthenticated_redirect(self, page, config):
        login = LoginPage(page, config)
        # Try to access dashboard without logging in
        page.goto(f"{config['base_url']}/company-admin/dashboard")
        page.wait_for_load_state("networkidle")

        assert login.is_on_login_page(), \
            f"Expected redirect to login, got: {page.url}"
        login.take_screenshot("unauthenticated_redirect")
