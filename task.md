# Proquro Automation Framework - Build Tasks

## Setup
- [/] Install dependencies (pytest, allure, pytest-xdist, etc.)
- [ ] Create project structure (folders + __init__.py files)
- [ ] Create config.yaml
- [ ] Create pytest.ini
- [ ] Create requirements.txt

## Core Framework
- [ ] conftest.py (shared fixtures: browser, login, screenshot-on-fail, cleanup)
- [ ] pages/base_page.py (BasePage with common methods)
- [ ] pages/login_page.py
- [ ] utils/helpers.py
- [ ] utils/cleanup.py (teardown/cleanup step)
- [ ] fixtures/test_data.json

## Page Objects
- [ ] pages/dashboard_page.py
- [ ] pages/team_management_page.py
- [ ] pages/department_page.py
- [ ] pages/role_management_page.py
- [ ] pages/cost_centre_page.py
- [ ] pages/indent_page.py
- [ ] pages/purchase_requisition_page.py
- [ ] pages/rfq_page.py
- [ ] pages/purchase_orders_page.py
- [ ] pages/vendor_page.py
- [ ] pages/purchase_invoice_page.py
- [ ] pages/item_master_page.py

## Test Files
- [ ] tests/auth/test_login.py
- [ ] tests/auth/test_user_creation.py (create users for other roles)
- [ ] tests/smoke/test_page_loads.py (all 20 pages)
- [ ] tests/functional/test_team_management.py
- [ ] tests/functional/test_department.py
- [ ] tests/functional/test_role_management.py
- [ ] tests/functional/test_cost_centre.py
- [ ] tests/functional/test_indent.py
- [ ] tests/functional/test_purchase_requisition.py
- [ ] tests/functional/test_rfq.py
- [ ] tests/functional/test_purchase_orders.py
- [ ] tests/functional/test_vendor.py
- [ ] tests/functional/test_purchase_invoice.py
- [ ] tests/functional/test_item_master.py
- [ ] tests/multi_user/test_multi_session.py

## Reporting
- [ ] Verify Allure installed and report generates
- [ ] Run full suite and generate first report
