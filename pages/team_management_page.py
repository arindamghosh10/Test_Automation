# -*- coding: utf-8 -*-
"""TeamManagementPage – /company-admin/team-invitation"""
import allure
from pages.base_page import BasePage


class TeamManagementPage(BasePage):
    URL = "/company-admin/team-invitation"

    SEARCH_INPUT   = 'input[placeholder*="Search by name"]'
    INVITE_BTN     = 'button:has-text("Invite Member")'
    BULK_INVITE    = 'button:has-text("Bulk Invite")'
    PENDING_TAB    = 'button:has-text("Pending Invitations")'
    HISTORY_TAB    = 'button:has-text("Invitation History")'
    TABLE_ROWS     = "table tbody tr"
    MODAL          = "[role='dialog'], .modal, [class*='modal']"

    def open(self):
        with allure.step("Open Team Management page"):
            self.navigate(self.URL)
            self.wait_for_heading("Team Invitations")

    def search(self, term: str):
        with allure.step(f"Search team members: {term}"):
            self.page.locator(self.SEARCH_INPUT).fill(term)
            self.page.wait_for_load_state("networkidle")

    def click_invite_member(self):
        with allure.step("Click 'Invite Member'"):
            self.page.locator(self.INVITE_BTN).click()

    def fill_invite_form(self, email: str, role: str, department: str = ""):
        with allure.step(f"Fill invite form: email={email}, role={role}"):
            # Email field in modal
            self.page.locator("input[type='email'], input[placeholder*='email']").last.fill(email)
            # Role dropdown
            role_sel = self.page.locator("select, [class*='select']").first
            role_sel.select_option(label=role) if role_sel else None

    def submit_invite(self):
        with allure.step("Submit invite form"):
            self.page.locator("button[type='submit'], button:has-text('Send'), button:has-text('Invite')").last.click()
            self.page.wait_for_load_state("networkidle")

    def get_pending_count(self) -> int:
        with allure.step("Get pending invitations count"):
            btn_text = self.page.locator(self.PENDING_TAB).first.inner_text()
            # Extract number from text like "Pending Invitations 2"
            import re
            nums = re.findall(r'\d+', btn_text)
            return int(nums[0]) if nums else 0

    def get_row_count(self) -> int:
        return self.page.locator(self.TABLE_ROWS).count()
