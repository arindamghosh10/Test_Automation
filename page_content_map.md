# Proquro – Full Page Content & Forms Map

**Environment:** https://stg.proquro.ai | **Account:** mobpark@yopmail.com (Company Admin)

---

## 1. Company Admin Dashboard
**URL:** `/company-admin/dashboard`

| Element | Details |
|---------|---------|
| **H1** | Company Administrator Dashboard |
| **H2 Sections** | User Management, System Alerts, Recent Activity, Department Overview, Pending Actions, Quick Actions |
| **Table** | DEPARTMENT \| USERS \| HEADS \| BUDGET \| UTILIZATION |
| **Quick Action Buttons** | Add User, New Department, Manage Roles, Workflow Config, Cost Centers, Approval Matrix |
| **Other Buttons** | Manage, View All Alerts, View All, Configure, Review All Pending Actions |

---

## 2. Team Management
**URL:** `/company-admin/team-invitation`

| Element | Details |
|---------|---------|
| **H1** | Team Invitations |
| **Table Columns** | INVITEE \| STATUS \| ROLE \| DEPARTMENT \| SENT \| ACTIONS |
| **Search Field** | `Search by name, email, department...` |
| **Status Tabs** | Pending Invitations 2, Invitation History |
| **Filter Dropdowns** | Pending, All Roles |
| **Action Buttons** | Bulk Invite, Invite Member |

---

## 3. Department
**URL:** `/company-admin/department/dashboard`

| Element | Details |
|---------|---------|
| **H1** | Department Management |
| **Table Columns** | DEPARTMENT \| DEPARTMENT HEAD \| USERS \| BUDGET \| UTILIZATION \| STATUS \| ACTIONS |
| **Search Field** | `Search departments...` |
| **Filter Dropdowns** | All Locations, All Status |
| **Action Buttons** | Add Department |

---

## 4. Role Management
**URL:** `/company-admin/role-management`

| Element | Details |
|---------|---------|
| **H1** | Role Management |
| **Search Field** | `Search roles by name or code...` |
| **Filter Dropdown** | Select (role type) |
| **Action Buttons** | + Create New Role |

---

## 5. Cost Centre
**URL:** `/company-admin/cost-center`

| Element | Details |
|---------|---------|
| **H1** | Cost Centers |
| **Table Columns** | COST CENTER \| TYPE \| LOCATION \| STATUS \| CREATED ON \| LAST UPDATED ON \| ACTIONS |
| **Search Field** | `Search cost centers...` |
| **Filter Dropdown** | Select (type/status) |
| **Action Buttons** | + Add Cost Center |

---

## 6. Indent Management
**URL:** `/company-admin/indent-dashboard`

| Element | Details |
|---------|---------|
| **H1** | Indent Management |
| **Search Field** | `Search indents...` |
| **Status Tabs** | All (28), Draft (7), Cancelled (0), Approved (21) |
| **Filter Dropdown** | Select |
| **Row Actions** | View, Edit |
| **Action Buttons** | + Create New Indent |

---

## 7. Need Identification (Purchase Requisition)
**URL:** `/company-admin/purchase-requisition`

| Element | Details |
|---------|---------|
| **H1** | Need Identification |
| **Table Columns** | PR ID \| PR DATE \| REQUESTOR \| DEPARTMENT \| COST CENTRE \| TYPE \| PRIORITY \| REQUIRED BY \| EST. AMOUNT \| STATUS \| APPROVAL STEP \| ACTIONS |
| **Search Field** | `Search PR ID, requestor…` |
| **Filter Dropdowns** | All Departments, Select (status) |
| **Action Buttons** | New PR |
| **Pagination** | 10 per page |

---

## 8. Purchase Contracts
**URL:** `/company-admin/purchase-contract`

| Element | Details |
|---------|---------|
| **H1** | Purchase Contracts |
| **Table Columns** | CONTRACT ID \| PO REF \| SUPPLIER \| TYPE \| VALUE \| STATUS \| APPROVAL \| SIGNATURE \| ACTIONS |
| **Search Field** | `Search contract ID, PO, supplier...` |
| **Status Tabs** | All 1, Draft 1 |
| **Filter Dropdown** | Select |
| **Action Buttons** | New Contract, Settings, Clear |

---

## 9. Goods Receipt (GRN)
**URL:** `/company-admin/grn`

| Element | Details |
|---------|---------|
| **H1** | Goods Receipt Notes |
| **Table Columns** | GRN # \| DATE \| PO REF \| SUPPLIER \| WAREHOUSE \| RECEIVED BY \| RECEIVED \| ACCEPTED \| QC \| STATUS \| SEQ# \| ACTIONS |
| **Search Field** | `Search GRN #, PO #, Supplier...` |
| **Filter Dropdown** | All Suppliers |
| **Action Buttons** | Create GRN |
| **Pagination** | 10 per page (pages 1, 2, 3) |

---

## 10. Store Material Issue
**URL:** `/company-admin/store-issue-management`

| Element | Details |
|---------|---------|
| **H1** | Material Issue Requests |
| **Table Columns** | PR NUMBER \| DATE \| REQUESTOR \| DEPT \| COST CENTRE \| ITEMS \| EST. VALUE \| PRIORITY \| REQ. BY \| STATUS \| ACTION |
| **Search Field** | `Search PR ID, requestor, item...` |
| **Filter Dropdown** | All Departments |
| **Action Buttons** | Continue |

---

## 11. RFQ Management
**URL:** `/company-admin/rfq-list`

| Element | Details |
|---------|---------|
| **H1** | RFQ Management |
| **Table Columns** | RFQ NUMBER \| RFQ TITLE \| STATUS \| PRIORITY \| BUDGET \| DEADLINE \| QUOTES \| CREATED \| QUOTE COMPARE |
| **Search Field** | `Search RFQs...` |
| **Status Tabs** | All RFQs 52, Draft 14, Published 2, Quotes Received 0, Under Review 0, Expired 36 |
| **Form Fields** | Checkbox (select rows), Select dropdown |
| **Row Actions** | View |
| **Pagination** | Pages 1–6 |

---

## 12. Auction Management
**URL:** `/company-admin/auction`

| Element | Details |
|---------|---------|
| **H1** | Auction Management |
| **Search Field** | `Search by title, auction number...` |
| **Status Tabs** | All Auctions 5, Live 1, Scheduled 1, Drafts 1, Closed 2 |
| **Filter Dropdown** | Select |
| **Action Buttons** | Create Auction, Refresh |

---

## 13. Purchase Orders
**URL:** `/company-admin/purchase-orders`

| Element | Details |
|---------|---------|
| **H1** | Purchase Orders |
| **Table Columns** | PO NUMBER \| DATE \| SUPPLIER \| SOURCE TYPE \| DEPARTMENT \| ITEMS \| GRAND TOTAL \| STATUS \| ACTIONS |
| **Search Field** | `Search PO, supplier, RFQ...` |
| **Status Tabs** | All, Draft, Acknowledged, Awaiting Response, Review Dispute, Rejected, Closed, Completed |
| **Row Actions** | Edit, View |
| **Action Buttons** | Export, + Create Stand Alone PO |

---

## 14. Vendor Dashboard
**URL:** `/company-admin/vendor-management`

| Element | Details |
|---------|---------|
| **H1** | Vendor Management |
| **Table Columns** | VENDOR \| SOURCE \| CATEGORY \| LOCATION \| STATUS \| TAGS \| RATING \| ORDERS \| ACTIONS |
| **Search Field** | `Search vendors...` |
| **Source Tabs** | My APL 7, Browse eVendor 16, Browse Marketplace 4 |
| **Other Buttons** | Invite Vendor, Multi-Source Select, Duplicates 0 |

---

## 15. Invite Vendor
**URL:** `/company-admin/invite`

| Element | Details |
|---------|---------|
| **H1** | Vendor Invitations |
| **Table Columns** | VENDOR \| STATUS \| SENT \| EXPIRES \| REMINDERS \| ACTIONS |
| **Search Field** | `Search vendors by name or email...` |
| **Filter Dropdown** | Select (status) |
| **Action Buttons** | Bulk Upload, + New Invitation |

---

## 16. Purchase Invoice
**URL:** `/company-admin/purchase-invoice`

| Element | Details |
|---------|---------|
| **H1** | Purchase Invoices |
| **Table Columns** | INVOICE # \| SUPPLIER INV # \| DATE \| SUPPLIER \| PO REF \| GRN REF \| GRAND TOTAL \| MATCH STATUS \| PAYMENT STATUS \| READY \| ACTIONS |
| **Search Field** | `Search by Invoice #, PO #, GRN #, Supplier...` |
| **Status Tabs** | All 8, Draft 0, Submitted 0, Matched 1, Mismatch 0, Ready for Payment 0, Paid 7, Cancelled 0 |
| **Form Fields** | Checkbox (select rows), Select dropdown |
| **Action Buttons** | Export, View |
| **Records Present** | PI-2026-00001 to PI-2026-00008 |

---

## 17. Store Management (Store Manager Dashboard)
**URL:** `/store_manager_menu/store-manager-dashboard`

| Element | Details |
|---------|---------|
| **H1** | Store Manager Dashboard |
| **H2 Sections** | Pending Stock Checks, Low Stock Alerts, Pending Goods Receipt, Inventory Summary, Recent Stock Issuances, Quick Actions |
| **Table Columns** | PO Number \| Supplier \| Items \| Expected \| Value \| Status \| Action |
| **Quick Actions** | Issue Stock, Create PR, Create GRN, Track, Stock Report, GRN List, Item Catalog |
| **Row Actions** | Details, Forward to Procurement, View All |

---

## 18. Item Master
**URL:** `/company-admin/item-master`

| Element | Details |
|---------|---------|
| **H1** | Item Master Management |
| **Table Columns** | SKU CODE \| ITEM NAME \| CATEGORY \| HSN \| UOM \| STOCK \| LAST PRICE \| STATUS \| ACTIONS |
| **Search Field** | `Search items by name, code, or HSN...` |
| **Filter Dropdowns** | Filter by status, Filter by category |
| **Action Buttons** | Add Item, Import CSV |

---

## 19. Supplier Dashboard
**URL:** `/supplier/dashboard`

> ⚠️ Note: This URL redirects to the **Company Admin Dashboard** for this account role.

Same content as page #1 (Company Admin Dashboard).

---

## 20. Company Profile
**URL:** `/company-admin/company-profile`

| Element | Details |
|---------|---------|
| **H1** | MOBILE PARK (company name) |
| **H2 Sections** | About Company |
| **Profile Tabs** | Overview, Business Details, Locations, Payment Terms, Delivery Terms, Plant List, Tolerance |
| **Action Buttons** | Edit, Manage Subscription |
