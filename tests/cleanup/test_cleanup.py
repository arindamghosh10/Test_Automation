# -*- coding: utf-8 -*-
"""
utils/cleanup.py
Cleanup utility — deletes all test data created during the test run.
Called via the session-scoped cleanup_registry fixture.
"""
import allure
import pytest
from pages.base_page import BasePage


@allure.suite("Cleanup")
@allure.feature("Test Data Cleanup")
class TestCleanup:
    """
    Cleanup tests run last (use pytest-ordering: @pytest.mark.last).
    They read the cleanup_registry and remove all test-created records.
    """

    @pytest.mark.cleanup
    @pytest.mark.order("last")
    @allure.title("Cleanup: Delete test departments")
    def test_cleanup_departments(self, logged_in_page, config, cleanup_registry):
        depts = cleanup_registry.get("departments", [])
        if not depts:
            pytest.skip("No test departments to clean up")

        base = BasePage(logged_in_page, config)
        base.navigate("/company-admin/department/dashboard")
        base.wait_for_heading("Department Management")

        for dept_name in depts:
            try:
                # Search for the dept
                logged_in_page.locator('input[placeholder*="Search departments"]').fill(dept_name)
                logged_in_page.wait_for_load_state("networkidle")
                import time; time.sleep(1)

                # Click delete/actions button on matching row
                row = logged_in_page.locator(f"table tr:has-text('{dept_name}')")
                if row.count() > 0:
                    actions_btn = row.locator("button:has-text('Delete'), button[aria-label*='delete'], button[title*='delete']")
                    if actions_btn.count() > 0:
                        actions_btn.first.click()
                        time.sleep(1)
                        # Confirm deletion if dialog appears
                        confirm = logged_in_page.locator("button:has-text('Confirm'), button:has-text('Delete'), button:has-text('Yes')")
                        if confirm.count() > 0:
                            confirm.first.click()
                            logged_in_page.wait_for_load_state("networkidle")
                        allure.attach(
                            f"Deleted department: {dept_name}",
                            name="cleanup_dept",
                            attachment_type=allure.attachment_type.TEXT
                        )
            except Exception as e:
                allure.attach(
                    f"Failed to delete {dept_name}: {str(e)}",
                    name="cleanup_error",
                    attachment_type=allure.attachment_type.TEXT
                )
        base.take_screenshot("cleanup_departments_done")

    @pytest.mark.cleanup
    @pytest.mark.order("last")
    @allure.title("Cleanup: Delete test items from Item Master")
    def test_cleanup_items(self, logged_in_page, config, cleanup_registry):
        items = cleanup_registry.get("items", [])
        if not items:
            pytest.skip("No test items to clean up")

        base = BasePage(logged_in_page, config)
        base.navigate("/company-admin/item-master")
        base.wait_for_heading("Item Master Management")

        for item_name in items:
            try:
                logged_in_page.locator('input[placeholder*="Search items"]').fill(item_name)
                logged_in_page.wait_for_load_state("networkidle")
                import time; time.sleep(1)

                row = logged_in_page.locator(f"table tr:has-text('{item_name}')")
                if row.count() > 0:
                    actions_btn = row.locator("button:has-text('Delete'), button[aria-label*='delete']")
                    if actions_btn.count() > 0:
                        actions_btn.first.click()
                        time.sleep(1)
                        confirm = logged_in_page.locator("button:has-text('Confirm'), button:has-text('Delete'), button:has-text('Yes')")
                        if confirm.count() > 0:
                            confirm.first.click()
                            logged_in_page.wait_for_load_state("networkidle")
            except Exception as e:
                allure.attach(f"Failed to delete item {item_name}: {str(e)}", name="cleanup_item_error",
                              attachment_type=allure.attachment_type.TEXT)
        base.take_screenshot("cleanup_items_done")

    @pytest.mark.cleanup
    @pytest.mark.order("last")
    @allure.title("Cleanup: Summary report of all created resources")
    def test_cleanup_summary(self, cleanup_registry):
        summary = []
        for key, items in cleanup_registry.items():
            summary.append(f"{key}: {len(items)} items")
        allure.attach(
            "\n".join(summary),
            name="cleanup_summary",
            attachment_type=allure.attachment_type.TEXT
        )
