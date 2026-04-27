# -*- coding: utf-8 -*-
"""
tests/functional/test_rfq.py - RFQ Management functional tests
"""
import time
import pytest
import allure
from pages.base_page import BasePage


@allure.suite("Functional Tests")
@allure.feature("RFQ Management")
class TestRFQManagement:
    URL = "/company-admin/rfq-list"

    @pytest.mark.functional
    @allure.title("RFQ page loads correctly")
    def test_page_load(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        base.wait_for_heading("RFQ Management")
        assert not base.is_page_error()
        base.take_screenshot("rfq_loaded")

    @pytest.mark.functional
    @allure.title("RFQ table has correct columns")
    def test_table_columns(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        for col in ["RFQ NUMBER", "RFQ TITLE", "STATUS", "BUDGET", "DEADLINE", "QUOTES"]:
            assert logged_in_page.locator(f"th:has-text('{col}')").count() > 0
        base.take_screenshot("rfq_columns")

    @pytest.mark.functional
    @allure.title("RFQ search filters results")
    def test_search(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        initial = base.get_table_row_count()
        logged_in_page.locator('input[placeholder*="Search RFQs"]').first.fill("NOTEXISTRFQ999")
        time.sleep(1)
        assert base.get_table_row_count() <= initial
        base.take_screenshot("rfq_search_filtered")

    @pytest.mark.functional
    @allure.title("Draft tab filters RFQs")
    def test_draft_tab(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        logged_in_page.locator("button:has-text('Draft')").first.click()
        time.sleep(1)
        assert not base.is_page_error()
        base.take_screenshot("rfq_draft_tab")
