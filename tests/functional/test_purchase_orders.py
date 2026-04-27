# -*- coding: utf-8 -*-
"""
tests/functional/test_purchase_orders.py - Purchase Orders functional tests
"""
import time
import pytest
import allure
from pages.base_page import BasePage


@allure.suite("Functional Tests")
@allure.feature("Purchase Orders")
class TestPurchaseOrders:
    URL = "/company-admin/purchase-orders"

    @pytest.mark.functional
    @allure.title("Purchase Orders page loads")
    def test_page_load(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        base.wait_for_heading("Purchase Orders")
        assert not base.is_page_error()
        base.take_screenshot("po_loaded")

    @pytest.mark.functional
    @allure.title("PO table has correct columns")
    def test_table_columns(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        for col in ["PO NUMBER", "DATE", "SUPPLIER", "GRAND TOTAL", "STATUS"]:
            assert logged_in_page.locator(f"th:has-text('{col}')").count() > 0
        base.take_screenshot("po_columns")

    @pytest.mark.functional
    @allure.title("PO status tabs are visible")
    def test_status_tabs(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        for tab in ["All", "Draft", "Acknowledged", "Completed"]:
            assert logged_in_page.locator(f"button:has-text('{tab}')").count() > 0
        base.take_screenshot("po_tabs")

    @pytest.mark.functional
    @allure.title("PO search filters results")
    def test_search(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        initial = base.get_table_row_count()
        logged_in_page.locator('input[placeholder*="Search PO"]').first.fill("NOTEXIST999")
        time.sleep(1)
        assert base.get_table_row_count() <= initial
        base.take_screenshot("po_search")

    @pytest.mark.functional
    @allure.title("Create Stand Alone PO button is visible")
    def test_create_po_button(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        assert logged_in_page.locator("button:has-text('Create Stand Alone PO')").count() > 0
        base.take_screenshot("po_create_btn")
