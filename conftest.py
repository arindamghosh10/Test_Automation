# -*- coding: utf-8 -*-
"""
conftest.py – Shared pytest fixtures for the Proquro automation suite.

Provides:
  - config       : Loaded config.yaml
  - browser      : Playwright browser instance (session-scoped)
  - page         : Fresh page per test
  - logged_in    : Page already authenticated as company_admin
  - screenshot_on_failure : Allure-attached screenshot on every failure
  - cleanup_registry : Collects created resource IDs for teardown
"""
import json
import os
import time
import pytest
import yaml
import allure

from playwright.sync_api import sync_playwright

# ── Load config ─────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def config():
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def test_data():
    data_path = os.path.join(os.path.dirname(__file__), "fixtures", "test_data.json")
    with open(data_path, "r") as f:
        return json.load(f)

# ── Playwright browser (session-scoped = one browser for entire test run) ────

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw

@pytest.fixture(scope="session")
def browser(playwright_instance, config):
    br = playwright_instance.chromium.launch(
        headless=config.get("headless", True),
        slow_mo=config.get("slow_mo", 0),
    )
    yield br
    br.close()

# ── Context + Page (function-scoped = fresh per test) ────────────────────────

@pytest.fixture(scope="function")
def context(browser, config):
    vp = config.get("viewport", {"width": 1440, "height": 900})
    ctx = browser.new_context(viewport=vp)
    yield ctx
    ctx.close()

@pytest.fixture(scope="function")
def page(context):
    pg = context.new_page()
    yield pg
    pg.close()

# ── Login helper ─────────────────────────────────────────────────────────────

def do_login(page, config, user_key="company_admin"):
    """Perform login and wait for the dashboard."""
    user = config["users"][user_key]
    base = config["base_url"]

    page.goto(f"{base}/sign-in?redirect=%2Fcompany-admin%2Fdashboard")
    page.wait_for_load_state("networkidle")

    page.locator('a:has-text("Securely Login With Email")').click()
    page.wait_for_load_state("networkidle")

    page.locator('input[type="email"], input[name="email"], input[name="username"]').first.fill(user["email"])
    page.locator('input[type="password"]').first.fill(user["password"])
    page.locator('button[type="submit"], button:has-text("Continue"), button:has-text("Sign in")').first.click()

    page.wait_for_url(f"**{user['expected_landing']}", timeout=config["timeouts"]["page_load"])
    page.wait_for_load_state("networkidle")
    return page

@pytest.fixture(scope="function")
def logged_in_page(page, config):
    """Returns a page already logged in as company_admin."""
    return do_login(page, config, "company_admin")

# ── Cleanup registry ─────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def cleanup_registry():
    """
    A shared dictionary where tests register resources they create.
    Cleanup tests will read this and delete those resources.

    Structure:
        {
          "departments": ["TEST_DEPT_abc123", ...],
          "cost_centres": ["TEST_CC_abc123", ...],
          "invitations": ["test_invite@yopmail.com", ...],
          ...
        }
    """
    registry = {
        "departments": [],
        "cost_centres": [],
        "team_invitations": [],
        "vendor_invitations": [],
        "indents": [],
        "purchase_requisitions": [],
        "items": [],
        "rfqs": [],
    }
    yield registry
    # After all tests, print summary of what was created
    print("\n[Cleanup Registry Summary]")
    for key, items in registry.items():
        if items:
            print(f"  {key}: {len(items)} items created → need cleanup")

# ── Screenshot on failure (Allure) ───────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        # Try to grab the page fixture from the test
        page = item.funcargs.get("page") or item.funcargs.get("logged_in_page")
        if page:
            try:
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name=f"failure_{item.name}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass

# ── Unique name helper ────────────────────────────────────────────────────────

def unique_name(prefix: str) -> str:
    """Generate a unique name with timestamp suffix for test data."""
    return f"{prefix}{int(time.time())}"
