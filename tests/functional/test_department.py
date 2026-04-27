# -*- coding: utf-8 -*-
"""
tests/functional/test_department.py
Functional tests for Department module.
"""
import time
import pytest
import allure
from conftest import unique_name
from pages.department_page import DepartmentPage


@allure.suite("Functional Tests")
@allure.feature("Department Management")
class TestDepartment:

    @allure.title("Department page loads correctly")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.functional
    def test_page_load(self, logged_in_page, config):
        dp = DepartmentPage(logged_in_page, config)
        dp.open()
        assert not dp.is_page_error()
        dp.take_screenshot("dept_loaded")

    @allure.title("Search filters department table")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.functional
    def test_search(self, logged_in_page, config):
        dp = DepartmentPage(logged_in_page, config)
        dp.open()
        initial_count = dp.get_row_count()
        dp.search("XXXXNOTEXISTING")
        time.sleep(1)
        filtered = dp.get_row_count()
        assert filtered <= initial_count
        dp.take_screenshot("dept_search_filtered")

    @allure.title("Add Department button opens form/modal")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.functional
    def test_add_department_opens_form(self, logged_in_page, config):
        dp = DepartmentPage(logged_in_page, config)
        dp.open()
        dp.click_add_department()
        time.sleep(1)
        modal = logged_in_page.locator("[role='dialog'], form, .modal, [class*='dialog']")
        assert modal.count() > 0, "Add Department form/modal should appear"
        dp.take_screenshot("dept_add_modal")

    @allure.title("Create new department (CRUD: Create)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.functional
    def test_create_department(self, logged_in_page, config, cleanup_registry):
        dp = DepartmentPage(logged_in_page, config)
        dp.open()
        dept_name = unique_name("TEST_DEPT_")

        dp.click_add_department()
        time.sleep(1)
        dp.fill_department_form(name=dept_name, budget="100000")
        dp.submit_form()
        time.sleep(2)

        cleanup_registry["departments"].append(dept_name)
        toast = dp.get_toast_message()

        assert dp.department_exists_in_table(dept_name) or "success" in toast.lower(), \
            f"Department '{dept_name}' should appear in table. Toast: '{toast}'"
        dp.take_screenshot("dept_created")

    @allure.title("Table has correct columns: DEPARTMENT, USERS, BUDGET, ACTIONS")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.functional
    def test_table_columns(self, logged_in_page, config):
        dp = DepartmentPage(logged_in_page, config)
        dp.open()
        for col in ["DEPARTMENT", "USERS", "BUDGET", "STATUS", "ACTIONS"]:
            assert logged_in_page.locator(f"th:has-text('{col}')").count() > 0, \
                f"Column '{col}' should be visible in table"
        dp.take_screenshot("dept_table_columns")
