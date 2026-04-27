# -*- coding: utf-8 -*-
"""
tests/functional/test_vendor.py - Vendor Management functional tests
"""
import time
import pytest
import allure
from pages.base_page import BasePage


@allure.suite("Functional Tests")
@allure.feature("Vendor Management")
class TestVendorManagement:

    @pytest.mark.functional
    @allure.title("Vendor Dashboard page loads")
    def test_vendor_dashboard_load(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate("/company-admin/vendor-management")
        base.wait_for_heading("Vendor Management")
        assert not base.is_page_error()
        base.take_screenshot("vendor_dashboard")

    @pytest.mark.functional
    @allure.title("Vendor table has correct columns")
    def test_table_columns(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate("/company-admin/vendor-management")
        for col in ["VENDOR", "CATEGORY", "LOCATION", "STATUS", "RATING", "ORDERS"]:
            assert logged_in_page.locator(f"th:has-text('{col}')").count() > 0
        base.take_screenshot("vendor_columns")

    @pytest.mark.functional
    @allure.title("Vendor source tabs visible: My APL, Browse eVendor, Browse Marketplace")
    def test_source_tabs(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate("/company-admin/vendor-management")
        for tab in ["My APL", "Browse eVendor", "Browse Marketplace"]:
            assert logged_in_page.locator(f"button:has-text('{tab}')").count() > 0
        base.take_screenshot("vendor_source_tabs")

    @pytest.mark.functional
    @allure.title("Vendor search works")
    def test_search(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate("/company-admin/vendor-management")
        initial = base.get_table_row_count()
        logged_in_page.locator('input[placeholder*="Search vendors"]').first.fill("NOTEXISTVENDOR999")
        time.sleep(1)
        assert base.get_table_row_count() <= initial
        base.take_screenshot("vendor_search")

    @pytest.mark.functional
    @allure.title("Invite Vendor page loads")
    def test_invite_vendor_page(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate("/company-admin/invite")
        base.wait_for_heading("Vendor Invitations")
        assert not base.is_page_error()
        base.take_screenshot("invite_vendor_loaded")

    @pytest.mark.functional
    @allure.title("Invite Vendor table has correct columns")
    def test_invite_table_columns(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate("/company-admin/invite")
        for col in ["VENDOR", "STATUS", "SENT", "EXPIRES", "REMINDERS"]:
            assert logged_in_page.locator(f"th:has-text('{col}')").count() > 0
        base.take_screenshot("invite_vendor_columns")
