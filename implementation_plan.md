# Proquro – Automation Testing Plan

## Overview

We already have:
- ✅ Login automation working
- ✅ All 20 pages mapped (URLs, forms, tables, buttons)
- ✅ Playwright + Python environment set up

The goal is to build a **professional, maintainable test suite** with HTML reports, multi-user support, and clear pass/fail results.

---

## Proposed Tech Stack

| Layer | Tool |
|-------|------|
| Browser automation | **Playwright (Python)** |
| Test framework | **pytest** (standard, flexible, great reporting) |
| Test reporting | **pytest-html** + **Allure** (rich HTML reports with screenshots) |
| Parallel execution | **pytest-xdist** (run multiple tests/users simultaneously) |
| Config/credentials | **YAML config file** (multiple user accounts) |
| Data | **JSON/CSV fixtures** (test data for forms) |

---

## Folder Structure

```
Proquro_testAutomation/
├── conftest.py                  # Shared fixtures (browser, login, config)
├── config.yaml                  # All user credentials, base URL
├── pytest.ini                   # pytest settings
│
├── tests/
│   ├── auth/
│   │   ├── test_login.py        # Login/logout, wrong creds, session
│   │   └── test_signup.py       # Sign up flow
│   │
│   ├── pages/
│   │   ├── test_dashboard.py
│   │   ├── test_team_management.py
│   │   ├── test_department.py
│   │   ├── test_role_management.py
│   │   ├── test_cost_centre.py
│   │   ├── test_indent.py
│   │   ├── test_purchase_requisition.py
│   │   ├── test_rfq.py
│   │   ├── test_purchase_orders.py
│   │   ├── test_vendor.py
│   │   ├── test_purchase_invoice.py
│   │   ├── test_item_master.py
│   │   └── ...
│   │
│   └── multi_user/
│       └── test_multi_session.py  # Parallel logins, role-based access
│
├── pages/                         # Page Object Model (POM)
│   ├── base_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── team_management_page.py
│   └── ...
│
├── fixtures/
│   ├── users.json                 # Multiple test user accounts
│   └── test_data.json            # Form data for CRUD tests
│
└── reports/
    ├── html/                      # pytest-html reports
    └── allure/                    # Allure rich reports
```

---

## Test Categories

### 1. Authentication Tests (`tests/auth/`)

| Test | What it checks |
|------|---------------|
| Valid login (Company Admin) | Lands on `/company-admin/dashboard` |
| Valid login (other roles) | Each user role lands on correct page |
| Invalid email/password | Error message shown |
| Login with empty fields | Validation errors shown |
| Session persistence | Refresh page → stays logged in |
| Logout | Redirects to sign-in |
| Multiple simultaneous logins | Different users in parallel sessions |

### 2. Page Load & Smoke Tests (`tests/pages/`)

For **every page**, automatically verify:
- Page loads with HTTP 200
- Correct H1 heading is visible
- No error boundaries or crash UI
- Key table/list renders (at least 0 rows, not an error)
- Search field is present and interactive

### 3. Form & CRUD Tests (per module)

Each module gets a dedicated test file covering:

| Test Pattern | Example |
|-------------|---------|
| **Create** | Fill form → Submit → Record appears in table |
| **Read/Search** | Type in search → Table filters correctly |
| **Update** | Click Edit → Change field → Save → Verify change |
| **Delete/Cancel** | Click Cancel/Delete → Confirm → Record removed |
| **Validation** | Submit empty required fields → Error messages shown |
| **Filter/Tab** | Click status tab → Table updates to matching records |

**Example for Team Management:**
- Click "Invite Member" → modal opens
- Fill email, select role + department → click Send
- Invitation appears in "Pending Invitations" tab
- Click Resend/Cancel on an invitation → verify result

### 4. Multi-User / Role-Based Tests (`tests/multi_user/`)

| Test | What it checks |
|------|---------------|
| Company Admin access | All 20 pages accessible |
| Department User access | Cannot access admin-only pages |
| Supplier/Vendor login | Lands on correct supplier dashboard |
| Concurrent sessions | 3 users logged in simultaneously (parallel) |
| Role restriction | Dept User tries to visit `/company-admin/role-management` → redirected or blocked |

---

## How Reports Will Work

### pytest-html (simple, immediate)
- Run: `pytest --html=reports/report.html --self-contained-html`
- Produces a single self-contained HTML file
- Shows: pass/fail per test, duration, error message, traceback

### Allure (rich, professional)
- Run: `pytest --alluredir=reports/allure`
- Then: `allure serve reports/allure`
- Shows: timeline, test steps, attached screenshots on failure, trend charts

**On every test failure**, the framework will:
1. Automatically take a screenshot
2. Attach it to the test report
3. Save the page HTML for debugging

---

## config.yaml (multi-user setup)

```yaml
base_url: "https://stg.proquro.ai"

users:
  company_admin:
    email: ""
    password: ""
    role: "company_admin"
    expected_landing: "/company-admin/dashboard"

  dept_user:
    email: "deptuser@yopmail.com"
    password: "TestPass123@"
    role: "department_user"
    expected_landing: "/department/dashboard"

  vendor:
    email: "vendor@yopmail.com"
    password: "VendorPass123@"
    role: "vendor"
    expected_landing: "/supplier/dashboard"
```

---

## Execution Plan

```bash
# Run all tests
pytest tests/ --html=reports/report.html -v

# Run only auth tests
pytest tests/auth/ -v

# Run only smoke tests (page load checks)
pytest tests/ -m smoke -v

# Run tests for multiple users in parallel
pytest tests/multi_user/ -n 3   # 3 parallel workers

# Run with Allure reporting
pytest tests/ --alluredir=reports/allure
allure serve reports/allure
```

---

## Open Questions

> [!IMPORTANT]
> 1. **User accounts:** Do you have test accounts for other roles (Dept User, Vendor, Store Manager, Finance User)? Or should I create test flows that register new users as part of the test?
> 2. **Scope of CRUD:** For destructive tests (create/delete records), should I use a dedicated test data set, or is it okay to create/delete real records on staging?
> 3. **Allure reporting:** Should I set up Allure (requires Java), or is the simpler pytest-html report enough for now?
> 4. **CI/CD:** Do you want tests to run automatically on a schedule (e.g., daily) or only on-demand?

---

## What I'll Build Next (after your approval)

1. Install `pytest`, `pytest-html`, `pytest-xdist`, `allure-pytest`
2. Set up `conftest.py` with shared login fixture and screenshot-on-failure hook
3. Build Page Object Models for each module
4. Write smoke tests for all 20 pages
5. Write functional tests per module (CRUD + validation)
6. Write multi-user parallel tests
7. Generate first full report
