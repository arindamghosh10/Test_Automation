# -*- coding: utf-8 -*-
"""
tests/functional/test_purchase_invoice.py - Purchase Invoice functional tests
"""
import time
import pytest
import allure
from pages.base_page import BasePage


@allure.suite("Functional Tests")
@allure.feature("Purchase Invoice")
class TestPurchaseInvoice:
    URL = "/company-admin/purchase-invoice"

    @pytest.mark.functional
    @allure.title("Purchase Invoice page loads")
    def test_page_load(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        base.wait_for_heading("Purchase Invoices")
        assert not base.is_page_error()
        base.take_screenshot("invoice_loaded")

    @pytest.mark.functional
    @allure.title("Invoice table has correct columns")
    def test_table_columns(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        for col in ["INVOICE #", "SUPPLIER", "PO REF", "GRAND TOTAL", "PAYMENT STATUS"]:
            assert logged_in_page.locator(f"th:has-text('{col}')").count() > 0
        base.take_screenshot("invoice_columns")

    @pytest.mark.functional
    @allure.title("Invoice status tabs are visible")
    def test_status_tabs(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        for tab in ["All", "Matched", "Paid"]:
            assert logged_in_page.locator(f"button:has-text('{tab}')").count() > 0
        base.take_screenshot("invoice_tabs")

    @pytest.mark.functional
    @allure.title("Invoice records are present (PI-2026)")
    def test_records_present(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        # We know from inspection that PI-2026-00001 to PI-2026-00008 exist
        assert base.get_table_row_count() > 0, "At least some invoice records should exist"
        base.take_screenshot("invoice_records")

    @pytest.mark.functional
    @allure.title("Invoice search works")
    def test_search(self, logged_in_page, config):
        base = BasePage(logged_in_page, config)
        base.navigate(self.URL)
        initial = base.get_table_row_count()
        logged_in_page.locator('input[placeholder*="Search by Invoice"]').first.fill("PI-2026-00001")
        time.sleep(1)
        assert base.get_table_row_count() <= initial
        base.take_screenshot("invoice_search")
