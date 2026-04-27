# -*- coding: utf-8 -*-
"""ItemMasterPage – /company-admin/item-master"""
import allure
from pages.base_page import BasePage


class ItemMasterPage(BasePage):
    URL = "/company-admin/item-master"

    SEARCH_INPUT  = 'input[placeholder*="Search items"]'
    ADD_ITEM_BTN  = 'button:has-text("Add Item")'
    IMPORT_BTN    = 'button:has-text("Import CSV")'
    TABLE_ROWS    = "table tbody tr"
    STATUS_FILTER = 'select[placeholder*="status"], select:has-text("Filter by status")'

    def open(self):
        with allure.step("Open Item Master page"):
            self.navigate(self.URL)
            self.wait_for_heading("Item Master Management")

    def search(self, term: str):
        with allure.step(f"Search items: {term}"):
            self.page.locator(self.SEARCH_INPUT).fill(term)
            self.page.wait_for_load_state("networkidle")

    def click_add_item(self):
        with allure.step("Click 'Add Item'"):
            self.page.locator(self.ADD_ITEM_BTN).click()

    def fill_item_form(self, name: str, sku: str, uom: str = "PCS"):
        with allure.step(f"Fill item form: name={name}, sku={sku}"):
            self.page.locator("input[name='name'], input[placeholder*='name'], input[placeholder*='Item']").last.fill(name)
            sku_input = self.page.locator("input[name='sku'], input[placeholder*='SKU'], input[placeholder*='code']")
            if sku_input.count() > 0:
                sku_input.first.fill(sku)

    def submit_form(self):
        with allure.step("Submit item form"):
            self.page.locator(
                "button[type='submit'], button:has-text('Save'), button:has-text('Create'), button:has-text('Add')"
            ).last.click()
            self.page.wait_for_load_state("networkidle")

    def item_exists_in_table(self, name: str) -> bool:
        with allure.step(f"Check if item '{name}' exists in table"):
            return self.page.locator(f"table td:has-text('{name}')").count() > 0

    def get_row_count(self) -> int:
        return self.page.locator(self.TABLE_ROWS).count()
