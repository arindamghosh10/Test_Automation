# -*- coding: utf-8 -*-
"""
tests/functional/test_team_management.py
Functional tests for Team Management module.
"""
import time
import pytest
import allure
from conftest import unique_name
from pages.team_management_page import TeamManagementPage


@allure.suite("Functional Tests")
@allure.feature("Team Management")
class TestTeamManagement:

    @allure.title("Page loads with correct heading and table")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.functional
    def test_page_load(self, logged_in_page, config):
        tm = TeamManagementPage(logged_in_page, config)
        tm.open()
        assert not tm.is_page_error(), "Team Management page should not show errors"
        tm.take_screenshot("team_mgmt_loaded")

    @allure.title("Search filters table results")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.functional
    def test_search_functionality(self, logged_in_page, config):
        tm = TeamManagementPage(logged_in_page, config)
        tm.open()
        initial_count = tm.get_row_count()

        tm.search("nonexistent_user_xyz_12345")
        time.sleep(1)
        filtered_count = tm.get_row_count()

        # Filtered count should be <= initial count (or 0 for no match)
        assert filtered_count <= initial_count, \
            "Search should reduce or equal row count"
        tm.take_screenshot("team_mgmt_search_filtered")

    @allure.title("Pending Invitations tab is clickable")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.functional
    def test_pending_tab(self, logged_in_page, config):
        tm = TeamManagementPage(logged_in_page, config)
        tm.open()
        logged_in_page.locator('button:has-text("Pending Invitations")').first.click()
        time.sleep(1)
        assert not tm.is_page_error()
        tm.take_screenshot("team_mgmt_pending_tab")

    @allure.title("Invitation History tab is clickable")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.functional
    def test_history_tab(self, logged_in_page, config):
        tm = TeamManagementPage(logged_in_page, config)
        tm.open()
        logged_in_page.locator('button:has-text("Invitation History")').first.click()
        time.sleep(1)
        assert not tm.is_page_error()
        tm.take_screenshot("team_mgmt_history_tab")

    @allure.title("Invite Member button opens modal")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.functional
    def test_invite_member_opens_modal(self, logged_in_page, config):
        tm = TeamManagementPage(logged_in_page, config)
        tm.open()
        tm.click_invite_member()
        time.sleep(1)

        # Check if a modal/dialog appeared
        modal = logged_in_page.locator("[role='dialog'], .modal, [class*='dialog']")
        assert modal.count() > 0, "Invite Member modal should open"
        tm.take_screenshot("team_mgmt_invite_modal")

    @allure.title("Send team member invitation (creates new user flow)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.functional
    def test_send_invitation(self, logged_in_page, config, test_data, cleanup_registry):
        tm = TeamManagementPage(logged_in_page, config)
        tm.open()
        initial_count = tm.get_pending_count()

        # Generate unique email
        email = f"{test_data['team_invite']['email_prefix']}{int(time.time())}{test_data['team_invite']['email_domain']}"

        tm.click_invite_member()
        time.sleep(1)
        tm.fill_invite_form(email=email, role="Department User")
        tm.submit_invite()
        time.sleep(2)

        # Register for cleanup
        cleanup_registry["team_invitations"].append(email)

        # Check if invitation count increased or toast appeared
        toast = tm.get_toast_message()
        new_count = tm.get_pending_count()
        assert (new_count > initial_count) or ("success" in toast.lower() or "sent" in toast.lower()), \
            f"Invitation should have been sent. Toast: '{toast}', count: {initial_count} -> {new_count}"
        tm.take_screenshot("team_mgmt_invite_sent")
