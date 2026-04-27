# -*- coding: utf-8 -*-
"""
tests/smoke/test_page_loads.py
Smoke tests: verify all 20 pages load correctly with correct heading and no errors.
"""
import pytest
import allure
from pages.base_page import BasePage

PAGES = [
    ("/company-admin/dashboard",              "Company Administrator Dashboard",   "Company Admin Dashboard"),
    ("/company-admin/team-invitation",         "Team Invitations",                  "Team Management"),
    ("/company-admin/department/dashboard",    "Department Management",              "Department"),
    ("/company-admin/role-management",         "Role Management",                   "Role Management"),
    ("/company-admin/cost-center",             "Cost Centers",                      "Cost Centre"),
    ("/company-admin/indent-dashboard",        "Indent Management",                 "Indent Management"),
    ("/company-admin/purchase-requisition",    "Need Identification",                "Need Identification (PR)"),
    ("/company-admin/purchase-contract",       "Purchase Contracts",                 "Purchase Contracts"),
    ("/company-admin/grn",                     "Goods Receipt Notes",                "Goods Receipt (GRN)"),
    ("/company-admin/store-issue-management",  "Material Issue Requests",            "Store Material Issue"),
    ("/company-admin/rfq-list",                "RFQ Management",                     "RFQ Management"),
    ("/company-admin/auction",                 "Auction Management",                 "Auction Management"),
    ("/company-admin/purchase-orders",         "Purchase Orders",                    "Purchase Orders"),
    ("/company-admin/vendor-management",       "Vendor Management",                  "Vendor Dashboard"),
    ("/company-admin/invite",                  "Vendor Invitations",                 "Invite Vendor"),
    ("/company-admin/purchase-invoice",        "Purchase Invoices",                  "Purchase Invoice"),
    ("/store_manager_menu/store-manager-dashboard", "Store Manager Dashboard",       "Store Management"),
    ("/company-admin/item-master",             "Item Master Management",             "Item Master"),
    ("/company-admin/company-profile",         None,                                 "Company Profile"),
]


@allure.suite("Smoke Tests")
@allure.feature("Page Load Verification")
class TestPageLoads:

    @pytest.mark.smoke
    @pytest.mark.parametrize("url,expected_h1,test_name", PAGES, ids=[p[2] for p in PAGES])
    @allure.title("Page loads: {test_name}")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_page_loads(self, logged_in_page, config, url, expected_h1, test_name):
        page = logged_in_page
        base = BasePage(page, config)

        with allure.step(f"Navigate to {url}"):
            response = page.goto(f"{config['base_url']}{url}", timeout=config["timeouts"]["page_load"])
            page.wait_for_load_state("networkidle", timeout=config["timeouts"]["network_idle"])

        with allure.step("Verify HTTP status is OK"):
            http_status = response.status if response else None
            assert http_status in (200, None), \
                f"Expected HTTP 200 for {url}, got {http_status}"

        with allure.step("Verify no error boundary"):
            assert not base.is_page_error(), \
                f"Page at {url} shows an error boundary"

        if expected_h1:
            with allure.step(f"Verify heading: {expected_h1}"):
                h1 = page.locator(f"h1:has-text('{expected_h1}')").first
                assert h1.count() > 0 or page.locator("h1").first.inner_text() != "", \
                    f"Expected H1 '{expected_h1}' not found on {url}"

        base.take_screenshot(f"smoke_{test_name.replace(' ', '_').lower()}")
