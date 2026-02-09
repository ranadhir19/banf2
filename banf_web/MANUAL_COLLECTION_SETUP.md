# BANF CMS Collections - Manual Setup Guide

## ⚠️ API Permissions Issue

The Wix API key needs "Manage Data Collections" permissions to create collections programmatically.
If you're getting 403 errors, the collections need to be created manually via Wix Dashboard.

---

## Manual Collection Creation Steps

### Go to Wix Dashboard
1. Log in to Wix.com
2. Go to your BANF site dashboard
3. Click **CMS** in the left sidebar
4. Click **+ Create Collection**

---

## Collection 1: Members

**Collection ID:** `Members`

| Field Name | Field Key | Type | Required |
|------------|-----------|------|----------|
| First Name | firstName | Text | Yes |
| Last Name | lastName | Text | Yes |
| Email | email | Text | Yes |
| Phone | phone | Text | No |
| Membership Type | membershipType | Text | Yes |
| Membership Status | membershipStatus | Text | Yes |
| Membership Start Date | membershipStartDate | Date | No |
| Membership End Date | membershipEndDate | Date | No |
| Total Paid | totalPaid | Number | No |
| Wix Member ID | wixMemberId | Text | No |
| Family Members | familyMembers | Text | No |
| Address | address | Text | No |
| City | city | Text | No |
| State | state | Text | No |
| Zip Code | zipCode | Text | No |
| Joined Date | joinedDate | Date | No |
| Notes | notes | Text | No |

**Permissions:** Admin only (read, write, insert, update, remove)

---

## Collection 2: Admins

**Collection ID:** `Admins`

| Field Name | Field Key | Type | Required |
|------------|-----------|------|----------|
| Email | email | Text | Yes |
| Password Hash | passwordHash | Text | Yes |
| Full Name | fullName | Text | Yes |
| Role | role | Text | Yes |
| Permissions | permissions | Text | No |
| Is Active | isActive | Boolean | Yes |
| Last Login | lastLogin | Date | No |
| Failed Attempts | failedAttempts | Number | No |
| Locked Until | lockedUntil | Date | No |
| Two Factor Enabled | twoFactorEnabled | Boolean | No |
| Created At | createdAt | Date | No |
| Created By | createdBy | Text | No |

**Permissions:** Admin only

**Default Admin Record:**
- Email: president@jaxbengali.org
- Full Name: BANF President
- Role: super_admin
- Is Active: true
- Password: (set securely via bcrypt hash)

---

## Collection 3: FinancialRecords

**Collection ID:** `FinancialRecords`

| Field Name | Field Key | Type | Required |
|------------|-----------|------|----------|
| Receipt Number | receiptNumber | Text | Yes |
| Transaction Type | transactionType | Text | Yes |
| Category | category | Text | Yes |
| Amount | amount | Number | Yes |
| Description | description | Text | No |
| Member ID | memberId | Text | No |
| Member Name | memberName | Text | No |
| Payment Method | paymentMethod | Text | No |
| Reference Number | referenceNumber | Text | No |
| Status | status | Text | Yes |
| Approved By | approvedBy | Text | No |
| Approved Date | approvedDate | Date | No |
| Notes | notes | Text | No |
| Transaction Date | transactionDate | Date | Yes |
| Fiscal Year | fiscalYear | Text | No |

**Permissions:** Admin only

**Category Values (for dropdown):**
- membership_dues
- event_registration
- donation
- sponsorship
- merchandise
- venue_rental
- catering
- supplies
- entertainment
- marketing
- administrative
- insurance
- utilities
- other

---

## Collection 4: Transactions

**Collection ID:** `Transactions`

| Field Name | Field Key | Type | Required |
|------------|-----------|------|----------|
| Transaction ID | transactionId | Text | Yes |
| Member ID | memberId | Text | Yes |
| Member Email | memberEmail | Text | Yes |
| Member Name | memberName | Text | No |
| Membership Type | membershipType | Text | No |
| Base Amount | baseAmount | Number | Yes |
| Processing Fee | processingFee | Number | No |
| Total Amount | totalAmount | Number | Yes |
| Payment Method | paymentMethod | Text | Yes |
| Payment Status | paymentStatus | Text | Yes |
| Wix Order ID | wixOrderId | Text | No |
| Payment Date | paymentDate | Date | No |
| Notes | notes | Text | No |

**Permissions:** Admin can read all, Members can read own

**Payment Status Values:**
- pending
- completed
- failed
- refunded
- cancelled

---

## Collection 5: ZellePayments

**Collection ID:** `ZellePayments`

| Field Name | Field Key | Type | Required |
|------------|-----------|------|----------|
| Member ID | memberId | Text | Yes |
| Member Email | memberEmail | Text | Yes |
| Member Name | memberName | Text | No |
| Amount | amount | Number | Yes |
| Confirmation Code | confirmationCode | Text | Yes |
| Transaction Date | transactionDate | Date | Yes |
| Membership Type | membershipType | Text | No |
| Status | status | Text | Yes |
| Verified By | verifiedBy | Text | No |
| Verified Date | verifiedDate | Date | No |
| Notes | notes | Text | No |

**Permissions:** Admin only

**Status Values:**
- pending_verification
- verified
- rejected

---

## Collection 6: AdminActivityLog

**Collection ID:** `AdminActivityLog`

| Field Name | Field Key | Type | Required |
|------------|-----------|------|----------|
| Admin ID | adminId | Text | Yes |
| Admin Email | adminEmail | Text | Yes |
| Action | action | Text | Yes |
| Action Details | actionDetails | Text | No |
| IP Address | ipAddress | Text | No |
| User Agent | userAgent | Text | No |
| Timestamp | timestamp | Date | Yes |

**Permissions:** Admin only (read only for most, write for system)

**Action Values:**
- login
- logout
- login_failed
- create_record
- update_record
- delete_record
- approve_payment
- reject_payment
- export_data
- change_settings

---

## After Creating Collections

### 1. Set Collection Permissions
For each collection:
1. Click the collection name
2. Click **Permissions & Privacy**
3. Set to **Admin only** (except Transactions which allows member read)

### 2. Create Default Admin
In the **Admins** collection, add a record:
```
email: president@jaxbengali.org
fullName: BANF President
role: super_admin
isActive: true
passwordHash: (leave empty for now, set via code)
createdAt: (current date)
```

### 3. Connect to Velo Backend
The backend code in `velo_backend/` references these collections by ID.
Make sure collection IDs match exactly.

### 4. Test Data Entry
Try adding a test record to each collection to verify fields work correctly.

---

## Updating the API Key (Optional)

If you want to use the setup script:

1. Go to Wix Dev Center: https://dev.wix.com/
2. Select your app or create a new one
3. Go to **OAuth** or **API Keys**
4. Generate a new key with these permissions:
   - `WIX_DATA.READ`
   - `WIX_DATA.WRITE`
   - `WIX_DATA.MANAGE_DATA_COLLECTIONS`
5. Update `WIX_API_KEY` in setup_payment_collections.py
6. Run the script again

---

## Wix Data API Reference

- Collections API: https://dev.wix.com/api/rest/wix-data/wix-data/data-collections
- Data Items API: https://dev.wix.com/api/rest/wix-data/wix-data/data-items
- Permission Levels: ADMIN, ANYONE, MEMBER

