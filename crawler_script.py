# -*- coding: utf-8 -*-
"""
Deep page inspector: logs in, navigates to each module page,
checks the REAL rendered visible text for errors vs content,
and takes a full-page screenshot.
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
import re
import time
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

BASE_URL = "https://stg.proquro.ai"
EMAIL    = ""
PASSWORD = ""

PAGES = [
    {"name": "Company Admin Dashboard",   "url": "/company-admin/dashboard"},
    {"name": "Team Management",           "url": "/company-admin/team-invitation"},
    {"name": "Department",                "url": "/company-admin/department/dashboard"},
    {"name": "Role Management",           "url": "/company-admin/role-management"},
    {"name": "Cost Centre",               "url": "/company-admin/cost-center"},
    {"name": "Indent Management",         "url": "/company-admin/indent-dashboard"},
    {"name": "Need Identification (PR)",  "url": "/company-admin/purchase-requisition"},
    {"name": "Purchase Contracts",        "url": "/company-admin/purchase-contract"},
    {"name": "Goods Receipt (GRN)",       "url": "/company-admin/grn"},
    {"name": "Store Material Issue",      "url": "/company-admin/store-issue-management"},
    {"name": "RFQ Management",            "url": "/company-admin/rfq-list"},
    {"name": "Auction Management",        "url": "/company-admin/auction"},
    {"name": "Purchase Orders",           "url": "/company-admin/purchase-orders"},
    {"name": "Vendor Dashboard",          "url": "/company-admin/vendor-management"},
    {"name": "Invite Vendor",             "url": "/company-admin/invite"},
    {"name": "Purchase Invoice",          "url": "/company-admin/purchase-invoice"},
    {"name": "Store Management",          "url": "/store_manager_menu/store-manager-dashboard"},
    {"name": "Item Master",               "url": "/company-admin/item-master"},
    {"name": "Supplier Dashboard",        "url": "/supplier/dashboard"},
    {"name": "Company Profile",           "url": "/company-admin/company-profile"},
]

def safe_name(text):
    return re.sub(r'[^a-zA-Z0-9_]', '_', text.lower())[:50]

# Next.js / generic error page selectors
ERROR_SELECTORS = [
    "div#__next_error__",          # Next.js build error overlay
    "[data-nextjs-error]",         # Next.js error boundary attr
    "body > div.error",            # generic error wrapper
    "h1:text-is('Application error: a client-side exception has occurred')",
    "h1:text-is('500')",           # standalone 500 heading
    "h2:text-is('Internal Server Error')",
]

def detect_error(page, http_status):
    """
    Returns an error string if a real error is detected, otherwise None.
    Uses HTTP status code + Next.js-specific error selectors.
    """
    # 1. Real HTTP error status
    if http_status and http_status >= 500:
        return f"HTTP {http_status} returned by server"
    if http_status and http_status == 404:
        return f"HTTP 404 - Page not found"

    # 2. Check for Next.js / framework error elements in the DOM
    for sel in ERROR_SELECTORS:
        try:
            if page.locator(sel).count() > 0:
                return f"Error element found: '{sel}'"
        except Exception:
            pass

    # 3. Check page title only
    title = page.title().lower()
    if title in ("error", "application error", "500 - internal server error", "404 - not found"):
        return f"Error page title: '{page.title()}'"

    return None

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()

    # ── Login ─────────────────────────────────────────────────────────────
    print("Logging in...")
    page.goto(f"{BASE_URL}/sign-in?redirect=%2Fcompany-admin%2Fdashboard")
    page.wait_for_load_state('networkidle')
    page.locator('a:has-text("Securely Login With Email")').click()
    page.wait_for_load_state('networkidle')
    page.locator('input[type="email"], input[name="email"], input[name="username"]').first.fill(EMAIL)
    page.locator('input[type="password"]').first.fill(PASSWORD)
    page.locator('button[type="submit"], button:has-text("Continue"), button:has-text("Sign in")').first.click()
    page.wait_for_url("**/company-admin/dashboard", timeout=20000)
    page.wait_for_load_state('networkidle')
    print("Logged in!\n")

    # ── Prepare output ─────────────────────────────────────────────────────
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    report = ["# Proquro – Full Page Inspection Report\n"]
    report.append("| # | Module | URL | Status | Issue |\n")
    report.append("|---|--------|-----|--------|-------|\n")

    STATUS_OK      = "[OK]"
    STATUS_ERROR   = "[ERROR]"
    STATUS_TIMEOUT = "[TIMEOUT]"
    STATUS_EXCEPT  = "[EXCEPTION]"
    STATUS_LOGIN   = "[REDIRECT TO LOGIN]"

    # ── Visit each page ────────────────────────────────────────────────────
    for idx, item in enumerate(PAGES, 1):
        name = item["name"]
        url  = BASE_URL + item["url"]
        fname = f"{safe_name(name)}_{idx}"

        print(f"[{idx}/{len(PAGES)}] {name}")
        status = STATUS_OK
        issue  = ""

        try:
            response = page.goto(url, timeout=20000)
            http_status = response.status if response else None
            page.wait_for_load_state('networkidle', timeout=20000)
            time.sleep(2)  # let JS-rendered content settle

            err = detect_error(page, http_status)
            if err:
                status = STATUS_ERROR
                issue  = err
            else:
                # Check if we got redirected to login
                if "sign-in" in page.url or "login" in page.url:
                    status = STATUS_LOGIN
                    issue  = f"Landed on: {page.url}"
                else:
                    status = STATUS_OK

        except PWTimeout:
            status = STATUS_TIMEOUT
            issue  = "Page did not load in 20 s"
        except Exception as e:
            status = STATUS_EXCEPT
            issue  = str(e)[:120]

        # Screenshot regardless
        ss_path = f"{screenshots_dir}/{fname}.png"
        try:
            page.screenshot(path=ss_path, full_page=True)
        except Exception:
            ss_path = "N/A"

        print(f"   -> {status}  {issue}")
        report.append(f"| {idx} | {name} | `{item['url']}` | {status} | {issue} |\n")

    # ── Write report ───────────────────────────────────────────────────────
    with open("full_inspection_report.md", "w", encoding="utf-8") as f:
        f.writelines(report)

    print("\nDone! Report saved to full_inspection_report.md")
    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as pw:
        run(pw)
