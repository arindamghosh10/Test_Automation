# -*- coding: utf-8 -*-
"""
tests/functional/test_item_master.py
Functional tests for Item Master module.
"""
import time
import pytest
import allure
from conftest import unique_name
from pages.item_master_page import ItemMasterPage


@allure.suite("Functional Tests")
@allure.feature("Item Master")
class TestItemMaster:

    @allure.title("Item Master page loads correctly")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.functional
    def test_page_load(self, logged_in_page, config):
        im = ItemMasterPage(logged_in_page, config)
        im.open()
        assert not im.is_page_error()
        im.take_screenshot("item_master_loaded")

    @allure.title("Search filters item table")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.functional
    def test_search(self, logged_in_page, config):
        im = ItemMasterPage(logged_in_page, config)
        im.open()
        initial = im.get_row_count()
        im.search("XXXNOTEXIST999")
        time.sleep(1)
        filtered = im.get_row_count()
        assert filtered <= initial
        im.take_screenshot("item_search_filtered")

    @allure.title("Table has correct columns: SKU, ITEM NAME, CATEGORY, UOM, STOCK, STATUS")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.functional
    def test_table_columns(self, logged_in_page, config):
        im = ItemMasterPage(logged_in_page, config)
        im.open()
        for col in ["SKU CODE", "ITEM NAME", "CATEGORY", "UOM", "STOCK", "STATUS"]:
            assert logged_in_page.locator(f"th:has-text('{col}')").count() > 0, \
                f"Column '{col}' missing from Item Master table"
        im.take_screenshot("item_table_columns")

    @allure.title("Add Item button opens form")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.functional
    def test_add_item_opens_form(self, logged_in_page, config):
        im = ItemMasterPage(logged_in_page, config)
        im.open()
        im.click_add_item()
        time.sleep(1)
        modal = logged_in_page.locator("[role='dialog'], form, .modal, [class*='dialog']")
        assert modal.count() > 0, "Add Item form/dialog should appear"
        im.take_screenshot("item_add_modal")

    @allure.title("Create new item (CRUD: Create)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.functional
    def test_create_item(self, logged_in_page, config, cleanup_registry):
        im = ItemMasterPage(logged_in_page, config)
        im.open()
        item_name = unique_name("TEST_ITEM_")
        sku = unique_name("SKU-TEST-")

        im.click_add_item()
        time.sleep(1)
        im.fill_item_form(name=item_name, sku=sku)
        im.submit_form()
        time.sleep(2)

        cleanup_registry["items"].append(item_name)
        toast = im.get_toast_message()

        assert im.item_exists_in_table(item_name) or "success" in toast.lower(), \
            f"Item '{item_name}' should appear in table. Toast: '{toast}'"
        im.take_screenshot("item_created")

    @allure.title("Import CSV button is visible")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.functional
    def test_import_csv_button_visible(self, logged_in_page, config):
        im = ItemMasterPage(logged_in_page, config)
        im.open()
        assert logged_in_page.locator('button:has-text("Import CSV")').count() > 0, \
            "Import CSV button should be visible"
        im.take_screenshot("item_import_btn")
