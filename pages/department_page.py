# -*- coding: utf-8 -*-
"""DepartmentPage – /company-admin/department/dashboard"""
import allure
from pages.base_page import BasePage


class DepartmentPage(BasePage):
    URL = "/company-admin/department/dashboard"

    SEARCH_INPUT  = 'input[placeholder*="Search departments"]'
    ADD_DEPT_BTN  = 'button:has-text("Add Department")'
    TABLE_ROWS    = "table tbody tr"

    def open(self):
        with allure.step("Open Department page"):
            self.navigate(self.URL)
            self.wait_for_heading("Department Management")

    def search(self, term: str):
        with allure.step(f"Search departments: {term}"):
            self.page.locator(self.SEARCH_INPUT).fill(term)
            self.page.wait_for_load_state("networkidle")

    def click_add_department(self):
        with allure.step("Click 'Add Department'"):
            self.page.locator(self.ADD_DEPT_BTN).click()

    def fill_department_form(self, name: str, budget: str = "100000"):
        with allure.step(f"Fill department form: name={name}"):
            name_input = self.page.locator(
                "input[name='name'], input[placeholder*='name'], input[placeholder*='Department']"
            ).last
            name_input.fill(name)
            budget_input = self.page.locator("input[name='budget'], input[placeholder*='budget']")
            if budget_input.count() > 0:
                budget_input.first.fill(budget)

    def submit_form(self):
        with allure.step("Submit department form"):
            self.page.locator(
                "button[type='submit'], button:has-text('Save'), button:has-text('Create')"
            ).last.click()
            self.page.wait_for_load_state("networkidle")

    def get_row_count(self) -> int:
        return self.page.locator(self.TABLE_ROWS).count()

    def department_exists_in_table(self, name: str) -> bool:
        with allure.step(f"Check if department '{name}' exists in table"):
            return self.page.locator(f"table td:has-text('{name}')").count() > 0
