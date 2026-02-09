# BANF Wix Payment & Accounting System
## Implementation Guide

### Overview

This document provides a complete guide for implementing the BANF payment and accounting system on Wix.

---

## Quick Start

### 1. Run Setup Script

```powershell
cd c:\projects\survey\banf_web
python setup_payment_collections.py
```

This creates 6 CMS collections:
- Members
- Admins
- FinancialRecords
- Transactions
- ZellePayments
- AdminActivityLog

### 2. Copy Backend Code to Wix

Copy contents of `velo_backend/` folder to Wix Editor:
1. Open Wix Editor → Dev Mode → Enable
2. Go to Backend section → Add new .jsw file
3. Copy each file's contents

**Files to copy:**
- `payment-processing.jsw`
- `accounting-ledger.jsw`
- `member-auth.jsw`
- `admin-auth.jsw`

### 3. Create Wix Pages

Create pages in Wix and copy Velo code from:
- `wix_pages/member-login.html` → /login
- `wix_pages/admin-login.html` → /admin/login
- `wix_pages/member-payment-portal.html` → /member-payment
- `wix_pages/admin-accounting-ledger.html` → /admin/accounting

### 4. Update Navigation

Add to header:
- **Member Login** button → `/login`
- **Join BANF** button → `/member-payment`

Add to footer (subtle):
- **Admin** link → `/admin/login`

---

## Feature Details

### Member Login System

**Registration Flow:**
1. User clicks "Join BANF"
2. Registers with email/password or social login
3. Selects membership type
4. Proceeds to payment

**Login Flow:**
1. User clicks "Member Login"
2. Enters credentials or uses social login
3. Redirected to member area

### Payment System with CC Fee Pass-Through

**Credit Card Fee Calculation:**
```javascript
// Processing fee: 2.9% + $0.30
const FEE_PERCENTAGE = 0.029;
const FEE_FIXED = 0.30;

// Formula: total = (base + 0.30) / (1 - 0.029)
function calculateTotalWithFee(baseAmount) {
    return (baseAmount + FEE_FIXED) / (1 - FEE_PERCENTAGE);
}
```

**Membership Pricing:**

| Membership Type | Base Price | With CC Fee |
|----------------|------------|-------------|
| EB-Family | $340.00 | $350.17 |
| EB-Couple | $300.00 | $309.45 |
| EB-Individual | $190.00 | $196.08 |
| EB-Student | $150.00 | $154.89 |
| Reg-Family | $215.00 | $221.80 |
| Reg-Couple | $200.00 | $206.35 |
| Reg-Individual | $150.00 | $154.89 |
| Reg-Student | $100.00 | $103.43 |

**Payment Options:**
1. **Credit Card** - Processed via Wix Pay, fee shown to member
2. **Zelle** - Direct bank transfer to banf.florida@gmail.com

### Admin Accounting Ledger

**Features:**
- Real-time dashboard with income/expense totals
- Transaction filtering (date, type, category)
- Running balance calculation
- CSV export for reports
- Add new records
- Approve pending transactions

**Access Control:**
- Only users with admin roles can access
- Roles: super_admin, president, vice_president, treasurer, secretary, ec_member, moderator

---

## Database Schema

### Members Collection
```
_id: String (auto)
email: String (required)
firstName: String
lastName: String
phone: String
membershipType: String (enum)
membershipStatus: String (active, expired, pending)
membershipExpiry: Date
totalPaid: Number
registrationDate: Date
lastLogin: Date
```

### Admins Collection
```
_id: String (auto)
email: String (required)
firstName: String
lastName: String
role: String (enum)
passwordHash: String
isActive: Boolean
createdAt: Date
lastLogin: Date
loginAttempts: Number
lockedUntil: Date
```

### FinancialRecords Collection
```
_id: String (auto)
date: Date
type: String (income, expense)
category: String (enum)
amount: Number
description: String
memberId: Reference
paymentMethod: String
referenceNumber: String
processedBy: String
status: String (pending, approved, rejected)
notes: String
createdAt: Date
```

### Transactions Collection
```
_id: String (auto)
memberId: Reference
memberEmail: String
memberName: String
membershipType: String
baseAmount: Number
processingFee: Number
totalAmount: Number
paymentMethod: String (credit_card, zelle)
paymentStatus: String
transactionId: String
createdAt: Date
processedAt: Date
notes: String
```

### ZellePayments Collection
```
_id: String (auto)
memberId: Reference
memberEmail: String
memberName: String
amount: Number
zelleConfirmationCode: String
zelleTransactionDate: Date
membershipType: String
status: String (pending, verified, rejected)
verifiedBy: String
verifiedAt: Date
notes: String
createdAt: Date
```

### AdminActivityLog Collection
```
_id: String (auto)
adminId: Reference
adminEmail: String
action: String
details: String
ipAddress: String
timestamp: Date
```

---

## Wix Editor Setup

### Step 1: Enable Dev Mode
1. Open Wix Editor
2. Click "Dev Mode" in top menu
3. Click "Turn on Dev Mode"

### Step 2: Create Backend Files
1. In Dev Mode sidebar, click "Backend"
2. Right-click → New .jsw file
3. Create each backend file

### Step 3: Connect CMS Collections
1. Add datasets to pages
2. Connect elements to dataset fields

### Step 4: Set Up Permissions
1. Go to Dashboard → CMS
2. For each collection, set permissions:
   - Members: Site Members can read own, Admin can read/write all
   - Admins: Admin only
   - FinancialRecords: Admin only
   - Transactions: Admin can read all, Members read own
   - ZellePayments: Admin only
   - AdminActivityLog: Admin only

### Step 5: Configure Wix Pay
1. Go to Dashboard → Accept Payments
2. Set up payment provider (Wix Payments or Stripe)
3. Enable credit card payments

### Step 6: Set Up Triggered Emails
1. Go to Dashboard → Automations
2. Create email triggers for:
   - New member registration
   - Payment confirmation
   - Membership renewal reminder

---

## Security Best Practices

1. **Password Hashing**: Use bcrypt (via wix-secrets)
2. **Rate Limiting**: Implement login attempt limits
3. **Session Management**: Use secure cookies
4. **HTTPS**: Wix enforces HTTPS automatically
5. **Input Validation**: Validate all user inputs
6. **Permission Checks**: Verify admin roles for protected operations

---

## Testing Checklist

- [ ] Member registration works
- [ ] Member login works
- [ ] Social login (Google/Facebook) works
- [ ] Membership selection shows correct prices
- [ ] CC fee calculation is correct
- [ ] Payment processing works
- [ ] Zelle payment recording works
- [ ] Admin login works with credentials
- [ ] Admin can view accounting ledger
- [ ] Admin can add financial records
- [ ] Admin can approve transactions
- [ ] CSV export works
- [ ] Logout works for both member and admin

---

## Troubleshooting

### "Collection not found" Error
- Run setup_payment_collections.py first
- Verify API credentials are correct

### Payment Not Processing
- Check Wix Pay setup in Dashboard
- Verify payment provider is configured
- Check browser console for errors

### Admin Cannot Login
- Verify admin record exists in Admins collection
- Check password hash is correct
- Reset password if needed

### CC Fee Not Showing
- Verify calculatePaymentWithFee function is imported
- Check if membership price data is loading

---

## Support

For technical issues:
- Review Wix Velo documentation
- Check browser console for JavaScript errors
- Verify CMS collections have correct fields

Contact: webmaster@jaxbengali.org
