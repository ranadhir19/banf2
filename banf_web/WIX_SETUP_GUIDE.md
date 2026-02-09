# BANF Wix Site Setup - Automation Guide

⚠️ **SECURITY WARNING**: Never store passwords in code files. Use environment variables or secure credential managers.

## Overview

This guide provides instructions for setting up the BANF application on your existing Wix site without modifying existing pages or structure.

---

## 📋 Pre-Setup Checklist

1. **Backup your existing site** - Use Wix's Site History feature
2. **Enable Velo** - Dev Mode must be turned on
3. **Review existing structure** - Document current pages and collections

---

## 🗂️ New Folder Structure (Add to existing site)

Create these **new folders** in your Wix site - do NOT modify existing folders:

```
Backend (Code Files):
├── backend/
│   ├── banf_members.jsw       (renamed from members.jsw)
│   ├── banf_events.jsw        (renamed from events.jsw)
│   ├── banf_finance.jsw       (renamed from finance.jsw)
│   ├── banf_admin.jsw         (renamed from admin.jsw)
│   ├── banf_complaints.jsw    (renamed from complaints.jsw)
│   ├── banf_surveys.jsw       (renamed from surveys.jsw)
│   ├── banf_radio.jsw         (renamed from radio.jsw)
│   ├── banf_magazine.jsw      (renamed from magazine.jsw)
│   ├── banf_guide.jsw         (renamed from guide.jsw)
│   ├── banf_email.jsw         (renamed from email.jsw)
│   ├── banf_sponsorship.jsw   (renamed from sponsorship.jsw)
│   └── banf_documents.jsw     (renamed from documents.jsw)

Pages (Add as new pages):
├── BANF Portal/               (new page folder)
│   ├── Member Dashboard
│   ├── Event Registration
│   ├── Magazine
│   ├── Jacksonville Guide
│   ├── Radio
│   ├── Surveys
│   ├── Complaints
│   └── Admin/
│       ├── Dashboard
│       ├── Members
│       ├── Events
│       ├── Sponsors
│       ├── Vendors
│       ├── Finance
│       ├── Documents
│       └── Reports
```

---

## 📦 CMS Collections to Create

Create these collections in Wix CMS (Content Manager):

### New Collections (27 total)

| Collection Name | Display Name | Purpose |
|----------------|--------------|---------|
| `BANF_Members` | BANF Members | Member profiles |
| `BANF_Admins` | BANF Admins | Administrator accounts |
| `BANF_Events` | BANF Events | Community events |
| `BANF_EventRegistrations` | Event Registrations | Event signups |
| `BANF_EventFeedback` | Event Feedback | Post-event surveys |
| `BANF_FinancialRecords` | Financial Records | Income/expenses |
| `BANF_ZellePayments` | Zelle Payments | Zelle verification |
| `BANF_Surveys` | Surveys | Survey definitions |
| `BANF_SurveyResponses` | Survey Responses | Survey answers |
| `BANF_Complaints` | Complaints | Anonymous complaints |
| `BANF_MeetingMinutes` | Meeting Minutes | EC meeting records |
| `BANF_EMagazines` | E-Magazines | Magazine issues |
| `BANF_EMagazineArticles` | Magazine Articles | Magazine content |
| `BANF_JacksonvilleGuide` | Jacksonville Guide | Local resources |
| `BANF_GuideReviews` | Guide Reviews | User reviews |
| `BANF_RadioStations` | Radio Stations | Station config |
| `BANF_RadioSchedule` | Radio Schedule | Show schedule |
| `BANF_BengaliSongs` | Bengali Songs | Song library |
| `BANF_SongRequests` | Song Requests | User requests |
| `BANF_Sponsors` | Sponsors | Sponsorship records |
| `BANF_Vendors` | Vendors | Vendor profiles |
| `BANF_VendorOrders` | Vendor Orders | Catering orders |
| `BANF_Documents` | Documents | Document storage |
| `BANF_DocumentActivityLog` | Document Log | Audit trail |
| `BANF_ImportantMessages` | Announcements | Important messages |
| `BANF_ActivityLog` | Activity Log | Admin actions |
| `BANF_RadioListenerLogs` | Listener Logs | Radio analytics |

---

## 🔧 Manual Setup Steps

### Step 1: Enable Velo (if not already enabled)
1. Open your Wix Editor
2. Click "Dev Mode" in the top menu
3. Click "Turn on Dev Mode"

### Step 2: Create Backend Folder
1. In the Code Panel, click "+" next to Backend
2. Create new .jsw files with "banf_" prefix
3. Copy code from `velo_backend/` folder (rename imports accordingly)

### Step 3: Create CMS Collections
1. Go to Content Manager
2. Click "+ Create Collection"
3. Name with "BANF_" prefix
4. Add fields from `collection_schemas.json`
5. Set permissions as specified

### Step 4: Create New Pages
1. Add new page folder "BANF Portal"
2. Create pages without touching existing pages
3. Link to new backend files

### Step 5: Set Up Triggered Emails
1. Go to Automations
2. Create email templates:
   - `banf_welcome_email`
   - `banf_event_confirmation`
   - `banf_payment_receipt`
   - etc.

---

## 🤖 Playwright Automation (Optional)

If you want to automate some setup steps, install Playwright:

```bash
pip install playwright
playwright install chromium
```

### Sample Automation Script

```python
# wix_setup_automation.py
# NOTE: Use environment variables for credentials!

import os
from playwright.sync_api import sync_playwright

# NEVER hardcode credentials - use environment variables
WIX_EMAIL = os.environ.get('WIX_EMAIL')
WIX_PASSWORD = os.environ.get('WIX_PASSWORD')

def setup_wix_collections():
    """
    Automate collection creation in Wix CMS
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Login to Wix
        page.goto('https://www.wix.com/signin')
        page.fill('input[type="email"]', WIX_EMAIL)
        page.fill('input[type="password"]', WIX_PASSWORD)
        page.click('button[type="submit"]')
        
        # Wait for dashboard
        page.wait_for_url('**/dashboard/**')
        
        # Navigate to Content Manager
        # ... automation steps ...
        
        browser.close()

if __name__ == '__main__':
    if not WIX_EMAIL or not WIX_PASSWORD:
        print("ERROR: Set WIX_EMAIL and WIX_PASSWORD environment variables")
        exit(1)
    setup_wix_collections()
```

### Set Environment Variables (Windows PowerShell)
```powershell
$env:WIX_EMAIL = "your-email@example.com"
$env:WIX_PASSWORD = "your-password"
```

---

## 📱 Mobile & Web Responsiveness

Wix provides automatic mobile responsiveness. Additional steps:

1. **Mobile Editor**: Use Wix Mobile Editor to fine-tune mobile layouts
2. **Breakpoints**: Set custom breakpoints in Editor
3. **Mobile Menu**: Configure mobile navigation
4. **Touch Targets**: Ensure buttons are tap-friendly (min 44px)

### Mobile-Specific Considerations

| Feature | Mobile Optimization |
|---------|---------------------|
| Event Registration | Simplified form, larger buttons |
| Magazine Reading | Swipe navigation, readable fonts |
| Radio Player | Floating mini-player |
| Document Upload | Camera integration for receipts |
| Admin Dashboard | Collapsible sidebar, card layout |

---

## 📄 Document Categories Setup

Create these document categories in the system:

### Financial Documents
- `EXPENSES` - Event expenses, venue, food, etc.
- `BILLS` - Vendor invoices, utility bills
- `RECEIPTS` - Payment confirmations
- `AUDIT` - Annual audit, compliance

### Organizational Documents
- `GOVERNANCE` - Bylaws, policies, procedures
- `MEETING_DOCS` - Agendas, minutes, reports
- `MEMBERSHIP` - Applications, directories

### Event Documents
- `EVENT_DOCS` - Plans, budgets, contracts
- `SPONSORSHIP_DOCS` - Agreements, artwork
- `VENDOR_CONTRACTS` - Food vendors, venues

### Media & Legal
- `PHOTOS` - Event photos by event type
- `MAGAZINE` - Published issues, archives
- `LEGAL` - Incorporation, tax exemption
- `INSURANCE` - Liability, event insurance
- `TAX` - 990 filings, tax returns

---

## ✅ Testing Checklist

After setup, test each feature:

### Public Features (No Login)
- [ ] View events list
- [ ] View magazine articles
- [ ] Search Jacksonville Guide
- [ ] Listen to radio
- [ ] Submit anonymous complaint
- [ ] Take anonymous survey

### Member Features (Login Required)
- [ ] Create account / Login
- [ ] Update profile
- [ ] Register for event
- [ ] Submit article
- [ ] Write guide review
- [ ] Take member survey

### Admin Features
- [ ] Access admin dashboard
- [ ] Create/edit events
- [ ] Manage sponsors
- [ ] Manage vendors
- [ ] Upload documents
- [ ] Generate reports
- [ ] View financial summary

---

## 🔒 Security Reminders

1. **Change your Wix password** after any sharing
2. **Enable 2FA** on your Wix account
3. **Review permissions** on all collections
4. **Test access levels** for each user role
5. **Regular backups** using Site History

---

*Document Version: 1.0*
*Last Updated: February 2026*
