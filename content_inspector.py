# -*- coding: utf-8 -*-
"""
Page Content Inspector for Proquro
Logs in, visits every module page, and extracts:
  - Page title / headings (h1, h2, h3)
  - Forms: all input labels, placeholders, field types
  - Buttons (text + type)
  - Tables: column headers
  - Key stat/metric cards (text from card-like elements)
  - Tabs / filter pills
Generates a markdown report: content_report.md
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os, re, time, json
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

BASE_URL = "https://stg.proquro.ai"
EMAIL    = "mobpark@yopmail.com"
PASSWORD = "Avromandal12345@"

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

def clean(text):
    """Strip and collapse whitespace."""
    return re.sub(r'\s+', ' ', (text or "").strip())

def get_texts(page, selector, limit=20):
    """Collect non-empty inner texts for a selector."""
    results = []
    try:
        elements = page.locator(selector).all()[:limit]
        for el in elements:
            t = clean(el.inner_text())
            if t and t not in results:
                results.append(t)
    except Exception:
        pass
    return results

def get_form_fields(page):
    """Extract label + input type + placeholder for all form inputs."""
    fields = []
    try:
        inputs = page.locator("input, select, textarea").all()[:50]
        for inp in inputs:
            try:
                field_type = inp.get_attribute("type") or inp.evaluate("el => el.tagName.toLowerCase()")
                placeholder = clean(inp.get_attribute("placeholder") or "")
                name_attr   = clean(inp.get_attribute("name") or "")
                aria_label  = clean(inp.get_attribute("aria-label") or "")
                # Try to find associated label
                input_id    = inp.get_attribute("id") or ""
                label_text  = ""
                if input_id:
                    try:
                        label_text = clean(page.locator(f"label[for='{input_id}']").first.inner_text())
                    except Exception:
                        pass
                display = label_text or aria_label or placeholder or name_attr or field_type
                if display and display not in [f["display"] for f in fields]:
                    fields.append({
                        "type": field_type,
                        "display": display,
                        "placeholder": placeholder,
                    })
            except Exception:
                pass
    except Exception:
        pass
    return fields

def get_table_headers(page):
    """Extract column headers from all visible tables."""
    headers = []
    try:
        tables = page.locator("table").all()[:5]
        for t in tables:
            ths = t.locator("th").all()[:20]
            row = [clean(th.inner_text()) for th in ths if clean(th.inner_text())]
            if row:
                headers.append(row)
    except Exception:
        pass
    return headers

def get_buttons(page):
    """Get all visible button labels."""
    btns = []
    try:
        for btn in page.locator("button, a[role='button'], [type='submit']").all()[:30]:
            t = clean(btn.inner_text())
            if t and len(t) < 60 and t not in btns:
                btns.append(t)
    except Exception:
        pass
    return btns

def get_tabs(page):
    """Get tab / pill labels."""
    tabs = []
    selectors = [
        "[role='tab']",
        "button.tab", ".tabs button",
        "nav a", ".pill", "[class*='tab']",
    ]
    for sel in selectors:
        found = get_texts(page, sel, 15)
        for f in found:
            if f and len(f) < 60 and f not in tabs:
                tabs.append(f)
    return tabs[:15]

def get_stat_cards(page):
    """Get metric card labels + values."""
    cards = []
    try:
        # Look for card-like structures with a label + big number
        card_els = page.locator("[class*='card'], [class*='stat'], [class*='metric'], [class*='kpi']").all()[:10]
        for card in card_els:
            t = clean(card.inner_text())
            if t and len(t) < 200 and t not in cards:
                cards.append(t)
    except Exception:
        pass
    return cards

def inspect_page(page):
    """Run all extractors on the current page."""
    return {
        "title":       page.title(),
        "h1":          get_texts(page, "main h1, #app-main-scroll h1, h1", 5),
        "h2":          get_texts(page, "main h2, #app-main-scroll h2, h2", 10),
        "h3":          get_texts(page, "main h3, #app-main-scroll h3, h3", 10),
        "tabs":        get_tabs(page),
        "form_fields": get_form_fields(page),
        "buttons":     get_buttons(page),
        "tables":      get_table_headers(page),
        "stat_cards":  get_stat_cards(page),
    }

def render_section(label, items):
    if not items:
        return f"- _{label}: none found_\n"
    return f"**{label}:**\n" + "\n".join(f"  - {i}" for i in items) + "\n"

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()

    # ── Login ──────────────────────────────────────────────────────────────
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

    os.makedirs("screenshots", exist_ok=True)
    report_lines = ["# Proquro – Page Content & Forms Report\n\n"]

    for idx, item in enumerate(PAGES, 1):
        name = item["name"]
        url  = BASE_URL + item["url"]
        safe = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())[:40]

        print(f"[{idx}/{len(PAGES)}] {name}")
        try:
            page.goto(url, timeout=20000)
            page.wait_for_load_state('networkidle', timeout=20000)
            time.sleep(2)

            data = inspect_page(page)
            ss   = f"screenshots/{safe}_{idx}.png"
            page.screenshot(path=ss, full_page=True)

        except Exception as e:
            print(f"  -> Error: {e}")
            data = {"title": "Error", "h1": [], "h2": [], "h3": [], "tabs": [],
                    "form_fields": [], "buttons": [], "tables": [], "stat_cards": []}
            ss = "N/A"

        # ── Build report section ───────────────────────────────────────────
        report_lines.append(f"---\n\n## {idx}. {name}\n\n")
        report_lines.append(f"**URL:** `{item['url']}`  \n")
        report_lines.append(f"**Page Title:** {data['title']}\n\n")

        if data['h1']:
            report_lines.append(render_section("Main Heading (H1)", data['h1']))
        if data['h2']:
            report_lines.append(render_section("Section Headings (H2)", data['h2']))
        if data['tabs']:
            report_lines.append(render_section("Tabs / Filters", data['tabs']))
        if data['stat_cards']:
            report_lines.append(render_section("Stat Cards / Metrics", data['stat_cards']))
        if data['tables']:
            for t_idx, cols in enumerate(data['tables'], 1):
                report_lines.append(f"**Table {t_idx} Columns:** {' | '.join(cols)}\n\n")
        if data['form_fields']:
            report_lines.append("**Form Fields:**\n")
            for f in data['form_fields']:
                hint = f" _(placeholder: {f['placeholder']})_" if f['placeholder'] else ""
                report_lines.append(f"  - [{f['type']}] {f['display']}{hint}\n")
            report_lines.append("\n")
        if data['buttons']:
            report_lines.append(render_section("Buttons / Actions", data['buttons']))
        report_lines.append(f"**Screenshot:** `{ss}`\n\n")
        print(f"   -> Done")

    with open("content_report.md", "w", encoding="utf-8") as f:
        f.writelines(report_lines)

    print("\nContent report saved to content_report.md")
    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as pw:
        run(pw)
