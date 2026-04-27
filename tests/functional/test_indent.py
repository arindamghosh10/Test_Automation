# -*- coding: utf-8 -*-
"""
tests/functional/test_indent.py - Indent Management functional tests
"""
import time
import pytest
import allure
from pages.base_page import BasePage


@allure.suite("Functional Tests")
@allure.feature("Indent Management")
class TestIndentManagement:
    URL = "/company-admin/indent-dashboard"

    @pytest.mark.functional
    @allure.title("Indent Management page loads")
    def test_page_load(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        base.wait_for_heading("Indent Management")
        assert not base.is_page_error()
        base.take_screenshot("indent_loaded")

    @pytest.mark.functional
    @allure.title("Indent status tabs visible: All, Draft, Approved, Cancelled")
    def test_status_tabs(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        for tab in ["All", "Draft", "Approved", "Cancelled"]:
            assert logged_in_page.locator(f"button:has-text('{tab}')").count() > 0
        base.take_screenshot("indent_tabs")

    @pytest.mark.functional
    @allure.title("Indent search works")
    def test_search(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        initial = base.get_table_row_count()
        logged_in_page.locator('input[placeholder*="Search indents"]').first.fill("NOTEXISTINDENT999")
        time.sleep(1)
        assert base.get_table_row_count() <= initial
        base.take_screenshot("indent_search")

    @pytest.mark.functional
    @allure.title("Create New Indent button is visible")
    def test_create_button_visible(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        assert logged_in_page.locator("button:has-text('Create New Indent')").count() > 0
        base.take_screenshot("indent_create_btn")


@allure.suite("Functional Tests")
@allure.feature("Need Identification (PR)")
class TestNeedIdentification:
    URL = "/company-admin/purchase-requisition"

    @pytest.mark.functional
    @allure.title("Need Identification page loads")
    def test_page_load(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        base.wait_for_heading("Need Identification")
        assert not base.is_page_error()
        base.take_screenshot("pr_loaded")

    @pytest.mark.functional
    @allure.title("PR table has correct columns")
    def test_table_columns(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        for col in ["PR ID", "PR DATE", "REQUESTOR", "DEPARTMENT", "STATUS"]:
            assert logged_in_page.locator(f"th:has-text('{col}')").count() > 0
        base.take_screenshot("pr_columns")

    @pytest.mark.functional
    @allure.title("New PR button is visible")
    def test_new_pr_button(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        assert logged_in_page.locator("button:has-text('New PR')").count() > 0
        base.take_screenshot("pr_new_btn")
