# BANF Web Platform - Comprehensive Feature & Workflow Documentation

## 📋 Document Information

| Property | Value |
|----------|-------|
| **Version** | 3.0 |
| **Last Updated** | February 8, 2026 |
| **Platform** | Wix Velo with Premium Business Plan |
| **Repository** | https://github.com/ranadhir19/banf1 |
| **Production Site** | https://www.jaxbengali.org |
| **DEV Site** | banf1 (Site ID: c13ae8c5-7053-4f2d-9a9a-371869be4395) |

---

## 🏛️ About BANF (Bengali Association of North Florida)

### Organization Overview

The **Bengali Association of North Florida (BANF)** is a vibrant cultural organization established to preserve and promote Bengali heritage, language, and traditions in the Jacksonville, Florida area. Founded with a mission to unite Bengali families and individuals, BANF has grown to become one of the most active cultural organizations in North Florida.

### Mission Statement

*"To preserve, promote, and celebrate Bengali culture, heritage, and language while fostering a sense of community among Bengali families and individuals in North Florida."*

### Key Statistics

| Metric | Value |
|--------|-------|
| **Active Families** | 150+ |
| **Annual Events** | 25+ |
| **Total Community Members** | 500+ |
| **Years of Service** | 15+ |

### Major Annual Events

1. **Durga Puja** - Our flagship event celebrating the goddess Durga
2. **Kali Puja** - Annual celebration of goddess Kali
3. **Saraswati Puja** - Celebration of goddess of knowledge
4. **Pohela Boishakh** - Bengali New Year celebration
5. **Annual Picnic** - Family gathering and outdoor activities
6. **Diwali Celebration** - Festival of lights
7. **Cultural Programs** - Regular music, dance, and literary events

---

## 🎯 Purpose of the BANF Digital Platform

### Vision

Transform BANF's operations from manual, paper-based processes to a fully integrated digital ecosystem that enhances member experience, streamlines administrative tasks, and enables transparent governance.

### Problems Solved by Digitization

| Traditional Challenge | Digital Solution | Efficiency Gain |
|----------------------|------------------|-----------------|
| Paper membership forms | Online registration with instant processing | **90% faster** |
| Manual payment tracking | Automated payment reconciliation | **95% accuracy** |
| Event registration chaos | QR-based check-in system | **80% time saved** |
| Spreadsheet finances | Real-time accounting ledger | **100% audit-ready** |
| Phone-tree communication | Automated SMS/Email notifications | **Instant reach** |
| Meeting minutes on paper | Digital archive with search | **Always accessible** |
| Sponsor tracking chaos | CRM-style sponsor management | **360° visibility** |
| Vendor coordination issues | Automated vendor portal | **Self-service** |

### Key Benefits of Automation

1. **Time Efficiency**: Reduce administrative overhead by 70%
2. **Transparency**: All members can access relevant information
3. **Accuracy**: Eliminate human errors in financial tracking
4. **Accessibility**: 24/7 access from any device
5. **Compliance**: Automatic audit trails for all transactions
6. **Communication**: Instant notifications to all stakeholders
7. **Engagement**: Self-service portals for members, sponsors, and vendors

---

## 👥 User Role Hierarchy & Access Matrix

### Role Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    SUPER ADMIN                               │
│              (IT Administrator / Developer)                  │
│  Full system access, technical configuration, all modules    │
├─────────────────────────────────────────────────────────────┤
│                    EXECUTIVE OFFICERS                        │
│   ┌─────────────┬──────────────┬────────────────┐           │
│   │  PRESIDENT  │  TREASURER   │  VICE PRESIDENT │           │
│   │ Full Access │  Financial   │   Most Access   │           │
│   │ + Approvals │  + Payments  │   - Sensitive   │           │
│   └─────────────┴──────────────┴────────────────┘           │
├─────────────────────────────────────────────────────────────┤
│                    EXECUTIVE COMMITTEE                       │
│   ┌──────────────┬──────────────┬───────────────┐           │
│   │  SECRETARY   │  EC MEMBER   │   MODERATOR   │           │
│   │   Minutes    │   Limited    │    Content    │           │
│   │ + Comms      │   Admin      │    Only       │           │
│   └──────────────┴──────────────┴───────────────┘           │
├─────────────────────────────────────────────────────────────┤
│                    MEMBER                                    │
│        Self-service, event registration, payments            │
├─────────────────────────────────────────────────────────────┤
│                    VISITOR                                   │
│          Public content only, anonymous complaints           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎭 Specialized Admin Roles (16 Feature-Specific Roles)

In addition to the core 7 administrative roles, BANF implements **16 specialized roles** for granular feature management. These roles work alongside existing admin roles to enable delegation.

### Specialized Role Hierarchy Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SPECIALIZED ADMIN ROLES                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─── CONTENT MANAGEMENT ────┐  ┌─── MEDIA MANAGEMENT ───────┐             │
│  │                           │  │                            │             │
│  │  📰 MAGAZINE_EDITOR       │  │  🎵 RADIO_MANAGER          │             │
│  │    ↳ Edit, publish        │  │    ↳ Full radio control    │             │
│  │    ↳ Manage issues        │  │    ↳ Schedule management   │             │
│  │                           │  │                            │             │
│  │  📝 MAGAZINE_REVIEWER     │  │  🎧 RADIO_DJ               │             │
│  │    ↳ Review submissions   │  │    ↳ Host shows           │             │
│  │    ↳ Approve articles     │  │    ↳ Create playlists     │             │
│  │                           │  │                            │             │
│  │  📚 GUIDE_EDITOR          │  │  🎬 VIDEO_COORDINATOR      │             │
│  │    ↳ Manage listings      │  │    ↳ Schedule videos      │             │
│  │    ↳ Approve reviews      │  │    ↳ Manage streaming     │             │
│  └───────────────────────────┘  │                            │             │
│                                 │  📸 GALLERY_MANAGER        │             │
│                                 │    ↳ Full photo access     │             │
│                                 │    ↳ Album management      │             │
│                                 └────────────────────────────┘             │
│                                                                              │
│  ┌─── OPERATIONS MANAGEMENT ─────────────────────────────────────────────┐ │
│  │                                                                        │ │
│  │  🎉 EVENT_COORDINATOR         🙋 VOLUNTEER_COORDINATOR                 │ │
│  │    ↳ Create/manage events       ↳ Assign volunteers                   │ │
│  │    ↳ Handle registrations       ↳ Track hours                         │ │
│  │                                                                        │ │
│  │  🏪 VENDOR_COORDINATOR        📊 SURVEY_COORDINATOR                    │ │
│  │    ↳ Manage vendor apps          ↳ Create surveys                     │ │
│  │    ↳ Assign booths               ↳ Analyze results                    │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌─── BUSINESS & ANALYTICS ───┐  ┌─── COMMUNITY & SOCIAL ────┐             │
│  │                            │  │                            │             │
│  │  💰 AD_MANAGER             │  │  🏠 COMMUNITY_LEAD         │             │
│  │    ↳ Manage campaigns      │  │    ↳ Charity initiatives   │             │
│  │    ↳ Review/approve ads    │  │    ↳ Career guidance       │             │
│  │    ↳ Track performance     │  │    ↳ Scholarships          │             │
│  │                            │  │                            │             │
│  │  📈 REPORT_ANALYST         │  │  📱 SOCIAL_MEDIA_MANAGER   │             │
│  │    ↳ Generate reports      │  │    ↳ Cross-platform posts  │             │
│  │    ↳ Schedule exports      │  │    ↳ Social ad campaigns   │             │
│  │                            │  │                            │             │
│  │  🔬 DATA_ANALYST           │  │                            │             │
│  │    ↳ Full analytics        │  │                            │             │
│  │    ↳ Predictive models     │  │                            │             │
│  └────────────────────────────┘  └────────────────────────────┘             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Specialized Roles Permission Matrix

| Role ID | Role Name | Department | Key Permissions |
|---------|-----------|------------|-----------------|
| `magazine_editor` | Magazine Editor | Content | Edit articles, publish issues, manage editions |
| `magazine_reviewer` | Magazine Reviewer | Content | Review submissions, approve/reject articles |
| `radio_manager` | Radio Manager | Media | Full radio control, schedule shows, manage DJs |
| `radio_dj` | Radio DJ | Media | Host shows, create playlists, manage requests |
| `video_coordinator` | Video Coordinator | Media | Schedule videos, manage streaming sessions |
| `gallery_manager` | Gallery Manager | Media | Full photo access, create albums, moderate |
| `event_coordinator` | Event Coordinator | Operations | Create events, manage registrations |
| `volunteer_coordinator` | Volunteer Coordinator | Operations | Assign volunteers, track hours |
| `vendor_coordinator` | Vendor Coordinator | Operations | Manage vendor applications, assign booths |
| `ad_manager` | Ad Manager | Business | Manage ad campaigns, approve ads, track metrics |
| `social_media_manager` | Social Media Manager | Community | Cross-platform posts, social campaigns |
| `community_lead` | Community Lead | Community | Charity initiatives, career programs |
| `report_analyst` | Report Analyst | Analytics | Generate reports, schedule exports |
| `data_analyst` | Data Analyst | Analytics | Full analytics access, predictive models |
| `guide_editor` | Guide Editor | Content | Manage Jacksonville Guide listings |
| `survey_coordinator` | Survey Coordinator | Operations | Create surveys, analyze results |

---

## 📊 Reporting Module

### Overview
Comprehensive report generation system for all BANF modules with time-based and event-wise reporting capabilities.

### Report Types (25+)

| Category | Report Type | Description | Frequency |
|----------|-------------|-------------|-----------|
| **Financial** | `financial_summary` | Overview of income/expenses | Monthly |
| | `income_statement` | Detailed income breakdown | Quarterly |
| | `expense_report` | Categorized expenses | Monthly |
| | `budget_variance` | Budget vs actual | Monthly |
| **Membership** | `membership_growth` | New/renewed members trend | Monthly |
| | `member_demographics` | Age, location analysis | Quarterly |
| | `retention_analysis` | Member retention rates | Quarterly |
| **Events** | `event_attendance` | Attendance per event | Per Event |
| | `event_revenue` | Revenue per event | Per Event |
| | `event_comparison` | Year-over-year comparison | Annually |
| **Volunteers** | `volunteer_hours` | Hours tracked by member | Monthly |
| | `volunteer_participation` | Engagement metrics | Quarterly |
| **Sponsors** | `sponsor_roi` | ROI calculation per sponsor | Per Event |
| | `sponsor_engagement` | Benefit utilization | Quarterly |
| **Advertising** | `ad_performance` | Impressions, clicks, conversions | Weekly |
| | `ad_revenue` | Revenue by campaign/advertiser | Monthly |
| **Community** | `donation_summary` | Charity donations tracked | Monthly |
| | `initiative_impact` | Program outcomes | Quarterly |

### Time Periods
- **Daily** - Real-time operational reports
- **Weekly** - Performance summaries
- **Monthly** - Standard reporting cycle
- **Quarterly** - Strategic reviews
- **Yearly** - Annual reports
- **Custom** - User-defined date ranges

### Export Formats
- 📊 **CSV** - Data analysis
- 📗 **Excel** - Formatted worksheets
- 📄 **PDF** - Executive summaries

---

## 📈 Insights & Analytics Module

### Dashboard Types

| Dashboard | Purpose | Primary Users |
|-----------|---------|---------------|
| **Executive Overview** | KPIs across all modules | President, VP |
| **Financial Dashboard** | Revenue, expenses, trends | Treasurer |
| **Membership Dashboard** | Growth, retention, engagement | Admin Team |
| **Event Dashboard** | Attendance, satisfaction | Event Coordinators |
| **Engagement Dashboard** | Activity metrics | Marketing Team |
| **Content Dashboard** | Magazine, radio, video stats | Content Managers |
| **Sponsor Dashboard** | ROI, benefit tracking | Sponsor Relations |
| **Custom Dashboard** | User-configured metrics | Any Admin |

### Key Performance Indicators (KPIs)

```
┌────────────────────────────────────────────────────────────────────────┐
│                         EXECUTIVE KPI OVERVIEW                         │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  📊 MEMBERSHIP          💰 FINANCIAL         🎉 EVENTS                │
│  ───────────────        ─────────────        ────────                 │
│  Total Members: 502     Revenue: $45,230     Total Events: 24        │
│  Growth Rate: +12%      Expenses: $38,100    Avg Attendance: 85      │
│  Retention: 89%         Surplus: $7,130      Satisfaction: 4.6/5     │
│  Active %: 76%          Budget Var: -2%      Upcoming: 3             │
│                                                                        │
│  📰 ENGAGEMENT          💼 SPONSORS          🏘️ COMMUNITY             │
│  ───────────────        ─────────────        ─────────────            │
│  Magazine Views: 1,240  Active: 18           Initiatives: 5          │
│  Radio Listeners: 89    Total Value: $25K    Donations: $8,450       │
│  Event RSVPs: 156       ROI Avg: 3.2x        Volunteers: 42          │
│  Survey Responses: 78   Renewals: 94%        Hours Logged: 680       │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Predictive Analytics

| Prediction Type | Model | Accuracy Target |
|-----------------|-------|-----------------|
| Membership Growth | Time-series forecasting | 85%+ |
| Event Attendance | Historical + seasonal | 80%+ |
| Revenue Forecast | Trend + pattern analysis | 75%+ |
| Churn Risk | Engagement scoring | 80%+ |

---

## 🏘️ Community Engagement Module

### Initiative Types

| Type | Description | Example Programs |
|------|-------------|------------------|
| **Charity** | Fundraising & donations | Food drives, disaster relief |
| **Career Guidance** | Professional development | Resume workshops, job fairs |
| **Education** | Learning programs | Bengali language classes |
| **Health & Wellness** | Health initiatives | Health camps, yoga sessions |
| **Environment** | Environmental programs | Clean-up drives, tree planting |
| **Cultural** | Heritage preservation | Traditional arts workshops |
| **Youth Programs** | Youth engagement | Summer camps, mentorship |
| **Senior Support** | Elder assistance | Tech help, social visits |
| **Scholarships** | Educational aid | Merit-based awards |

### Donation Tracking

| Donation Type | Description | Receipt Generation |
|---------------|-------------|-------------------|
| **Monetary** | Cash/card donations | Auto-generated |
| **Goods** | Physical items | Manual + inventory |
| **Services** | Professional services | Service agreement |
| **Volunteer Hours** | Time contribution | Hour logging |

### Career Guidance Features

- **Mentorship Matching** - Connect professionals with job seekers
- **Resume Review Sessions** - Professional resume assistance
- **Mock Interviews** - Practice interview sessions
- **Industry Networking** - Sector-specific meetups
- **Job Board** - Community job postings

### Scholarship Management

- **Application Portal** - Online applications
- **Review Workflow** - Committee evaluation
- **Award Tracking** - Disbursement management
- **Recipient Communication** - Status updates

---

## 📺 Advertisement Management Module (Google Ads-like System)

### Overview
Complete advertising platform for vendors and sponsors to reach BANF community members across website, social media, and email channels.

### Ad Types

| Type | Format | Placement Options |
|------|--------|-------------------|
| 🖼️ **Banner** | 728x90, 300x250 | Home hero, event pages |
| 📏 **Sidebar** | 300x600, 160x600 | All pages sidebar |
| 🎯 **Popup** | 500x500 modal | Site-wide (limited) |
| 🎬 **Video** | 15-30 sec | Pre-roll, in-content |
| 📝 **Native** | Content-style | Magazine, guide |
| ⭐ **Sponsored** | Featured listings | Events, directory |
| 🎠 **Carousel** | Multi-image | Social media |
| ✉️ **Newsletter** | Email placement | Weekly digest |
| 📱 **Social** | Platform-specific | FB, IG, Twitter |

### Ad Placements

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEBSITE PLACEMENTS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────┐                   │
│  │           HOME_HERO (728x90)             │  Premium          │
│  └──────────────────────────────────────────┘                   │
│                                                                  │
│  ┌───────────────────────────┐  ┌────────────┐                  │
│  │                           │  │  SIDEBAR   │                  │
│  │    MAIN CONTENT AREA      │  │  (300x250) │                  │
│  │                           │  │            │                  │
│  │    - Event pages          │  │  Rotating  │                  │
│  │    - Magazine articles    │  │  ads       │                  │
│  │    - Member directory     │  │            │                  │
│  │                           │  └────────────┘                  │
│  └───────────────────────────┘                                  │
│                                                                  │
│  ┌──────────────────────────────────────────┐                   │
│  │           HOME_FOOTER (728x90)           │  Standard         │
│  └──────────────────────────────────────────┘                   │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                    SOCIAL MEDIA PLACEMENTS                       │
├─────────────────────────────────────────────────────────────────┤
│  📘 Facebook    📸 Instagram    🐦 Twitter    💼 LinkedIn        │
│  📺 YouTube     ✉️ Newsletter                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Billing Models

| Model | Description | Best For |
|-------|-------------|----------|
| **CPM** | Cost Per 1000 Impressions | Brand awareness |
| **CPC** | Cost Per Click | Traffic campaigns |
| **CPV** | Cost Per View (video) | Video ads |
| **CPA** | Cost Per Action | Conversions |
| **Flat Rate** | Fixed price per period | Premium placements |
| **Sponsorship** | Event/content sponsorship | Major sponsors |

### Campaign Management

| Feature | Description |
|---------|-------------|
| **Campaign Creation** | Set budgets, dates, targeting |
| **Ad Creative Upload** | Multiple formats supported |
| **Audience Targeting** | Member demographics, interests |
| **Budget Management** | Daily/total limits, bidding |
| **Performance Tracking** | Impressions, clicks, conversions |
| **A/B Testing** | Creative variations |
| **Automated Reporting** | Daily/weekly summaries |
| **Invoice Generation** | Automatic billing |

### Ad Review Workflow

```
┌─────────┐    ┌─────────────┐    ┌──────────┐    ┌────────┐
│  Draft  │───▶│ Pending     │───▶│ Approved │───▶│ Active │
│         │    │ Review      │    │          │    │        │
└─────────┘    └─────────────┘    └──────────┘    └────────┘
                     │                                  │
                     ▼                                  ▼
               ┌──────────┐                      ┌──────────┐
               │ Rejected │                      │ Completed│
               │          │                      │ /Expired │
               └──────────┘                      └──────────┘
```

---

### Detailed Role Permissions

#### 1. SUPER ADMIN (IT Administrator)
**Full system access with technical capabilities**

| Permission Category | Access Level |
|---------------------|--------------|
| System Configuration | ✅ Full |
| Database Management | ✅ Full |
| User Management | ✅ Full |
| All Financial Operations | ✅ Full |
| API Configuration | ✅ Full |
| Backup & Recovery | ✅ Full |
| Integration Settings | ✅ Full |
| Security Settings | ✅ Full |

**Shared Responsibilities:**
- Event Management coordination
- Member data administration
- Vendor/Sponsor system management

---

#### 2. PRESIDENT
**Highest organizational authority with full operational access**

| Permission Category | Access Level |
|---------------------|--------------|
| All Admin Functions | ✅ Full |
| Financial Approvals (>$1000) | ✅ Approve |
| Budget Finalization | ✅ Approve |
| Member Suspension | ✅ Approve |
| Executive Decisions | ✅ Final Authority |
| Contract Signing | ✅ Authorize |
| Sponsor Agreements | ✅ Final Approve |

**Approval Workflows Requiring President:**
- Large expense approvals (>$1000)
- Member expulsion decisions
- Contract amendments
- Budget reallocation (>10%)
- New initiative approvals

---

#### 3. TREASURER
**Financial authority with payment and accounting access**

| Permission Category | Access Level |
|---------------------|--------------|
| Payment Verification | ✅ Full |
| Expense Approvals (<$1000) | ✅ Approve |
| Financial Reports | ✅ Generate |
| Budget Management | ✅ Modify |
| Tax Documents | ✅ Full Access |
| Bank Reconciliation | ✅ Full |
| Sponsor Payments | ✅ Record |
| Vendor Payments | ✅ Process |
| Member Read-Only | ✅ View Only |

**Sensitive Workflows for Treasurer:**
- Zelle payment verification
- Credit card reconciliation
- Expense reimbursements
- Budget tracking
- Annual financial reports
- Tax documentation

---

#### 4. VICE PRESIDENT
**Operational authority with most admin access**

| Permission Category | Access Level |
|---------------------|--------------|
| Members Management | ✅ Full |
| Events Management | ✅ Full |
| Meetings Management | ✅ Full |
| Financial View | ✅ View Only |
| Reports Generation | ✅ Full |
| Complaints Handling | ✅ Full |

**Vice President Cannot:**
- Approve payments over $500
- Access tax documents
- Modify financial records
- Change admin roles

---

#### 5. SECRETARY
**Communications and documentation authority**

| Permission Category | Access Level |
|---------------------|--------------|
| Meeting Minutes | ✅ Full |
| Email Communications | ✅ Send |
| Newsletter Management | ✅ Full |
| Member Read-Only | ✅ View |
| Reports Generation | ✅ View |
| Announcements | ✅ Create/Edit |

---

#### 6. EC MEMBER
**Limited administrative access for committee work**

| Permission Category | Access Level |
|---------------------|--------------|
| Events Management | ✅ Edit (assigned) |
| Meeting View | ✅ Read Only |
| Member View | ✅ Read Only |
| Survey Creation | ✅ Create |

---

#### 7. MODERATOR
**Content management and complaint handling**

| Permission Category | Access Level |
|---------------------|--------------|
| Complaint Management | ✅ Handle/Respond |
| Content Moderation | ✅ Approve/Reject |
| Magazine Articles | ✅ Review |
| Guide Listings | ✅ Moderate |

---

## 📊 Complete Feature Matrix by Role

### Legend
- ✅ = Full Access
- 👁️ = View Only
- ❌ = No Access
- 🔐 = Requires Approval

| Feature | Visitor | Member | Moderator | EC Member | Secretary | Vice President | Treasurer | President | Super Admin |
|---------|:-------:|:------:|:---------:|:---------:|:---------:|:--------------:|:---------:|:---------:|:-----------:|
| **MEMBERSHIP** |
| View membership info | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Register as member | ✅ | - | - | - | - | - | - | - | - |
| Update own profile | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| View member directory | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Manage all members | ❌ | ❌ | ❌ | ❌ | 👁️ | ✅ | 👁️ | ✅ | ✅ |
| Verify new members | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Suspend members | ❌ | ❌ | ❌ | ❌ | ❌ | 🔐 | ❌ | ✅ | ✅ |
| **EVENTS** |
| View events | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Register for events | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create events | ❌ | ❌ | ❌ | 🔐 | ❌ | ✅ | ❌ | ✅ | ✅ |
| Edit events | ❌ | ❌ | ❌ | 🔐 | ❌ | ✅ | ❌ | ✅ | ✅ |
| Manage registrations | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Check-in attendees | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ |
| **PAYMENTS** |
| Pay own fees | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| View own history | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Verify payments | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| View all payments | ❌ | ❌ | ❌ | ❌ | ❌ | 👁️ | ✅ | ✅ | ✅ |
| Process refunds | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **FINANCE** |
| View public budget | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Record transactions | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Approve expenses (<$500) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Approve expenses (<$1000) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🔐 | ✅ | ✅ |
| Approve expenses (>$1000) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Generate reports | ❌ | ❌ | ❌ | ❌ | ❌ | 👁️ | ✅ | ✅ | ✅ |
| **E-MAGAZINE** |
| Read articles | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Submit articles | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Review articles | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Publish magazine | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| **JACKSONVILLE GUIDE** |
| Browse places | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Submit listings | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Write reviews | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Moderate content | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| **COMMUNITY RADIO** |
| Listen to stream | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Request songs | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Manage schedule | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| View analytics | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| **SURVEYS** |
| Take public surveys | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Take member surveys | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create surveys | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ |
| View results | ❌ | ❌ | ❌ | 🔐 | ❌ | ✅ | ❌ | ✅ | ✅ |
| **COMPLAINTS** |
| Submit anonymous | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Check own status | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| View all complaints | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Respond to complaints | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| **MEETINGS** |
| View public minutes | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| View full minutes | ❌ | ❌ | ❌ | 👁️ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create/Edit minutes | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **SPONSORS** |
| View sponsors | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Manage sponsors | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Approve sponsors | ❌ | ❌ | ❌ | ❌ | ❌ | 🔐 | ✅ | ✅ | ✅ |
| **VENDORS** |
| Apply as vendor | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Manage vendors | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Approve vendors | ❌ | ❌ | ❌ | ❌ | ❌ | 🔐 | ✅ | ✅ | ✅ |
| **VOLUNTEERS** |
| Register as volunteer | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Manage volunteers | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Assign tasks | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ |
| **ADMIN** |
| View dashboard | ❌ | ❌ | ❌ | ❌ | 👁️ | ✅ | ✅ | ✅ | ✅ |
| Manage admins | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| System settings | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 🔄 Approval Workflows with Role Hierarchy

### 1. Payment Approval Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    PAYMENT SUBMITTED                             │
│                   (Member/External)                              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TREASURER REVIEW                              │
│            - Verify Zelle confirmation                           │
│            - Match amount to invoice                             │
│            - Check payment method                                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
      Amount ≤ $500              Amount > $500
              │                           │
              ▼                           ▼
┌─────────────────────┐     ┌─────────────────────────────────────┐
│ TREASURER APPROVES  │     │     Amount > $1000?                  │
│    Direct                 │     ├── YES → PRESIDENT APPROVAL      │
│                     │     │     └── NO  → TREASURER + VP APPROVAL │
└──────────┬──────────┘     └───────────────────────────────────────┘
           │                                    │
           ▼                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PAYMENT RECORDED                              │
│        - Update ledger                                           │
│        - Send receipt to payer                                   │
│        - Update member/sponsor status                            │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Expense Reimbursement Workflow

```
┌────────────────────┐
│ REQUEST SUBMITTED  │
│   by EC Member     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐     Amount > $1000?
│ TREASURER REVIEWS  │─────────────────────┐
│ - Valid receipt    │                     │
│ - Budget category  │     NO              │ YES
│ - Available funds  │     │               │
└─────────┬──────────┘     ▼               ▼
          │         ┌────────────┐  ┌────────────────┐
          │         │ TREASURER  │  │   PRESIDENT    │
          │         │  APPROVES  │  │   MUST APPROVE │
          │         └─────┬──────┘  └───────┬────────┘
          │               │                 │
          └───────────────┴────────┬────────┘
                                   │
                                   ▼
                        ┌────────────────────┐
                        │ PAYMENT PROCESSED  │
                        │ - Record expense   │
                        │ - Issue payment    │
                        └────────────────────┘
```

### 3. New Member Approval Workflow

```
┌────────────────────┐
│  NEW REGISTRATION  │
│   + Payment Info   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ AUTOMATIC CHECKS   │
│ - Duplicate email  │
│ - Payment received │
│ - Required fields  │
└─────────┬──────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
  PASS        FAIL
    │           │
    ▼           ▼
┌──────────┐ ┌──────────────┐
│ PENDING  │ │ NEEDS REVIEW │
│ PAYMENT  │ │ (Admin)      │
│ VERIFY   │ └──────┬───────┘
└────┬─────┘        │
     │              │
     ▼              │
┌────────────┐      │
│ TREASURER  │      │
│ VERIFIES   │      │
│ PAYMENT    │◄─────┘
└────┬───────┘
     │
     ▼
┌────────────────────┐
│ VICE PRESIDENT     │
│ or PRESIDENT       │
│ - Final approval   │
│ - Verify details   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  MEMBER ACTIVE     │
│ - Welcome email    │
│ - Access granted   │
└────────────────────┘
```

### 4. Sponsor Approval Workflow

```
┌─────────────────────┐
│ SPONSOR APPLICATION │
│   (Self-service)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  VICE PRESIDENT     │
│  INITIAL REVIEW     │
│  - Business verify  │
│  - Tier appropriate │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     │           │
     ▼           ▼
  TIER <       TIER ≥
  GOLD         GOLD
     │           │
     ▼           ▼
┌──────────┐ ┌──────────────┐
│   VP     │ │  PRESIDENT   │
│ APPROVES │ │  MUST APPROVE│
└────┬─────┘ └──────┬───────┘
     │              │
     └──────┬───────┘
            │
            ▼
┌─────────────────────┐
│  TREASURER RECORDS  │
│  - Invoice created  │
│  - Benefits tracked │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  SPONSOR ACTIVE     │
│  - Portal access    │
│  - Logo uploaded    │
│  - Benefits start   │
└─────────────────────┘
```

### 5. Vendor Approval Workflow

```
┌─────────────────────┐
│  VENDOR APPLICATION │
│   (Public form)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   AUTOMATIC CHECK   │
│   - Existing app?   │
│   - Required docs?  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐     Food Vendor?
│   VICE PRESIDENT    │─────────────────┐
│   REVIEWS           │                 │
│   - Business type   │     NO          │ YES
│   - Products        │     │           │
└──────────┬──────────┘     │           ▼
           │                │    ┌────────────────┐
           │                │    │ HEALTH PERMIT  │
           │                │    │ VERIFICATION   │
           │                │    │ (Required)     │
           │                │    └───────┬────────┘
           │                │            │
           ▼                ▼            │
┌─────────────────────────────────────────────────┐
│            TREASURER REVIEWS                     │
│     - Booth fee payment                          │
│     - Insurance documents                        │
│     - Contract terms                             │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│            VENDOR APPROVED                       │
│     - Booth assigned                             │
│     - Portal access                              │
│     - Event coordination                         │
└─────────────────────────────────────────────────┘
```

---

## 🛠️ Complete Feature List by Module

### Module 1: Membership Management

#### Features for VISITORS
- [ ] View membership tiers and benefits
- [ ] View membership pricing
- [ ] Start registration process
- [ ] Contact for membership inquiries

#### Features for MEMBERS
- [ ] Complete profile management
- [ ] Family member additions/updates
- [ ] Membership renewal
- [ ] Payment history view
- [ ] Receipt downloads
- [ ] Dietary preferences
- [ ] Communication preferences
- [ ] Event registration history

#### Features for ADMINS (Vice President, President, Super Admin)
- [ ] View all members list
- [ ] Advanced search and filters
- [ ] Member verification
- [ ] Status changes (active/suspended/expired)
- [ ] Bulk communications
- [ ] Export member data (CSV/Excel)
- [ ] Membership statistics dashboard
- [ ] Overdue fee tracking
- [ ] Renewal reminders

---

### Module 2: Event Management

#### Features for VISITORS
- [ ] View upcoming events calendar
- [ ] View event details (date, time, location, pricing)
- [ ] View past event galleries
- [ ] View event venue maps

#### Features for MEMBERS
- [ ] Register for events with guest count
- [ ] Member pricing display
- [ ] Add dietary restrictions
- [ ] Cancel registration (before deadline)
- [ ] View "My Registrations"
- [ ] Submit event feedback
- [ ] Download event tickets

#### Features for ADMINS
- [ ] Create new events
- [ ] Edit event details
- [ ] Set pricing (regular/member)
- [ ] Set registration deadlines
- [ ] Manage capacity limits
- [ ] View all registrations
- [ ] Export attendee lists
- [ ] QR code check-in
- [ ] Mark attendance
- [ ] Send event reminders
- [ ] Feature events on homepage
- [ ] View feedback summary
- [ ] Create event budgets
- [ ] Track event expenses

---

### Module 3: Financial Management

#### Features for VISITORS
- [ ] View published annual reports (if enabled)

#### Features for MEMBERS
- [ ] Pay membership fees online
- [ ] Pay event registration fees
- [ ] Submit Zelle payment confirmations
- [ ] View personal payment history
- [ ] Download receipts

#### Features for TREASURER
- [ ] Verify Zelle payments
- [ ] Record income/expense transactions
- [ ] Categorize transactions
- [ ] Approve expenses (<$1000)
- [ ] Generate financial reports
- [ ] View financial dashboard
- [ ] Budget tracking
- [ ] Export financial data
- [ ] Credit card fee calculations
- [ ] Reconciliation tools

#### Features for PRESIDENT
- [ ] Approve large expenses (>$1000)
- [ ] Budget finalization
- [ ] View all financial reports
- [ ] Audit access

---

### Module 4: E-Magazine (প্রতিবিম্ব)

#### Features for VISITORS
- [ ] Browse all published issues
- [ ] Read full articles
- [ ] Search articles by title/author
- [ ] Filter by category
- [ ] View popular articles

#### Features for MEMBERS
- [ ] Submit articles for review
- [ ] Track submission status
- [ ] View editor feedback
- [ ] Update drafts

#### Features for ADMINS (Moderator, VP, President)
- [ ] Review submitted articles
- [ ] Provide feedback
- [ ] Approve/reject articles
- [ ] Create magazine issues
- [ ] Add articles to issues
- [ ] Publish magazines
- [ ] Reorder articles
- [ ] Track article views

---

### Module 5: Jacksonville Newcomer Guide

#### Features for VISITORS
- [ ] Browse all categories (restaurants, grocers, temples, etc.)
- [ ] Search by name/keyword
- [ ] View business details
- [ ] Filter Bengali-friendly places
- [ ] Location-based search
- [ ] View community ratings

#### Features for MEMBERS
- [ ] Submit new listings
- [ ] Write reviews
- [ ] Rate places
- [ ] Track listing approval status

#### Features for ADMINS (Moderator, VP)
- [ ] Review listing submissions
- [ ] Approve/reject listings
- [ ] Edit listing details
- [ ] Feature places on homepage
- [ ] Moderate reviews
- [ ] Manage categories

---

### Module 6: Community Radio

#### Features for VISITORS
- [ ] Listen to live stream
- [ ] View current show info
- [ ] View weekly schedule
- [ ] Browse song library
- [ ] Submit song requests

#### Features for ADMINS
- [ ] Configure stream settings
- [ ] Update station status
- [ ] Manage show schedule
- [ ] Add songs to library
- [ ] View/approve requests
- [ ] View listener statistics

---

### Module 7: Surveys & Feedback

#### Features for VISITORS
- [ ] Take public/anonymous surveys
- [ ] Submit anonymous feedback

#### Features for MEMBERS
- [ ] Take member-only surveys
- [ ] View survey results (if enabled)

#### Features for ADMINS (EC Member, VP, President)
- [ ] Create new surveys
- [ ] Edit survey questions
- [ ] Set survey visibility
- [ ] Activate/deactivate surveys
- [ ] Clone survey templates
- [ ] View all responses
- [ ] Export response data
- [ ] Survey analytics dashboard
- [ ] Send survey invitations

---

### Module 8: Anonymous Complaint System

#### Features for ALL USERS
- [ ] Submit anonymous complaints
- [ ] Category selection (financial, operational, personal, other)
- [ ] Priority indication
- [ ] Receive complaint ID + access code
- [ ] Check complaint status
- [ ] Add follow-up messages

#### Features for ADMINS (Moderator, VP, President)
- [ ] View all complaints
- [ ] Filter by status/category/priority
- [ ] Assign complaints to team members
- [ ] Update complaint status
- [ ] Respond to complainants
- [ ] Mark complaints resolved
- [ ] View resolution statistics

---

### Module 9: Meeting Minutes

#### Features for MEMBERS
- [ ] View public meeting summaries
- [ ] Search meeting archives

#### Features for SECRETARY
- [ ] Create meeting minutes
- [ ] Edit meeting content
- [ ] Add confidential sections
- [ ] Record attendees
- [ ] Set action items
- [ ] Schedule next meeting

#### Features for EXECUTIVE ADMINS
- [ ] View full minutes including confidential
- [ ] Track action item progress
- [ ] Approve minutes for publication

---

### Module 10: Sponsorship Management

#### Features for VISITORS
- [ ] View sponsor tiers and benefits
- [ ] Submit sponsor application

#### Features for SPONSORS (via portal)
- [ ] View sponsorship status
- [ ] Upload logo and materials
- [ ] Track benefit fulfillment
- [ ] View upcoming events
- [ ] Contact coordinator

#### Features for ADMINS (VP, Treasurer, President)
- [ ] Review applications
- [ ] Set tier assignments
- [ ] Record pledges
- [ ] Record payments
- [ ] Track benefit delivery
- [ ] Magazine ad management
- [ ] Food sponsorship tracking
- [ ] Contact history logging
- [ ] Sponsorship reports
- [ ] Export sponsor data

---

### Module 11: Vendor Management

#### Features for VENDORS
- [ ] Submit vendor application
- [ ] Provide business details
- [ ] Upload required documents
- [ ] View booth assignment
- [ ] Track payment status
- [ ] Receive event updates

#### Features for ADMINS (VP, Treasurer)
- [ ] Review applications
- [ ] Verify health permits (food vendors)
- [ ] Assign booths
- [ ] Process payments
- [ ] Rate vendor performance
- [ ] Store contracts
- [ ] Track Bengali-owned businesses
- [ ] View vendor history

---

### Module 12: Volunteer Management

#### Features for VISITORS/MEMBERS
- [ ] Register as volunteer
- [ ] Select skills and availability
- [ ] Indicate task preferences
- [ ] View assigned tasks
- [ ] Log volunteer hours

#### Features for ADMINS (EC Member, VP)
- [ ] View all volunteers
- [ ] Create volunteer tasks
- [ ] Assign volunteers to tasks
- [ ] Schedule shifts
- [ ] Track hours
- [ ] Send reminders
- [ ] Award recognition badges
- [ ] Generate volunteer reports

---

### Module 13: Document Management

#### Features for MEMBERS
- [ ] View public documents
- [ ] Download permitted files

#### Features for ADMINS
- [ ] Upload documents
- [ ] Categorize (expenses, bills, audit, governance)
- [ ] Tag with keywords
- [ ] Set access levels (public/member/admin/confidential)
- [ ] Link to events/sponsors
- [ ] Version control
- [ ] Archive documents
- [ ] Search repository
- [ ] Bulk operations
- [ ] Storage monitoring

---

### Module 14: Communication Hub

#### Features for MEMBERS
- [ ] View announcements
- [ ] Manage email preferences
- [ ] Receive notifications

#### Features for SECRETARY
- [ ] Create announcements
- [ ] Set priority/type
- [ ] Set expiry dates
- [ ] Target audience selection
- [ ] Newsletter management

#### Features for ADMINS
- [ ] Send bulk emails
- [ ] SMS notifications
- [ ] Push notifications
- [ ] Communication templates

---

### Module 15: Admin Dashboard

#### Features for ALL ADMINS (by permission level)
- [ ] Real-time statistics widgets
- [ ] Pending items queue
- [ ] Quick action buttons
- [ ] Activity feed
- [ ] Charts and graphs
- [ ] Recent registrations
- [ ] Upcoming events
- [ ] Financial summary
- [ ] Complaint alerts

#### Features for SUPER ADMIN only
- [ ] User role management
- [ ] System configuration
- [ ] API settings
- [ ] Backup management
- [ ] Integration settings
- [ ] Security logs

---

## 📋 User Acceptance Test Checklist

### Phase 1: Visitor Journey Tests

| Test ID | Test Case | Expected Result | Status |
|---------|-----------|-----------------|--------|
| V-001 | Visit homepage as guest | Homepage loads with all sections | ⬜ |
| V-002 | View upcoming events | Event list displays correctly | ⬜ |
| V-003 | View event details | All event info visible | ⬜ |
| V-004 | Browse e-magazine | Articles display correctly | ⬜ |
| V-005 | Search Jacksonville guide | Search results appear | ⬜ |
| V-006 | Listen to radio | Stream plays | ⬜ |
| V-007 | Submit anonymous complaint | Complaint ID received | ⬜ |
| V-008 | Check complaint status | Status displays with code | ⬜ |
| V-009 | Take public survey | Response recorded | ⬜ |
| V-010 | Start registration | Registration form loads | ⬜ |
| V-011 | View sponsor information | Sponsor tiers display | ⬜ |
| V-012 | Submit vendor application | Application submitted | ⬜ |

### Phase 2: Member Journey Tests

| Test ID | Test Case | Expected Result | Status |
|---------|-----------|-----------------|--------|
| M-001 | Complete registration | Account created | ⬜ |
| M-002 | Login to account | Dashboard access | ⬜ |
| M-003 | Update profile | Changes saved | ⬜ |
| M-004 | Add family member | Family updated | ⬜ |
| M-005 | Register for event | Registration confirmed | ⬜ |
| M-006 | Pay membership fee | Payment processed | ⬜ |
| M-007 | Submit Zelle payment | Confirmation recorded | ⬜ |
| M-008 | Download receipt | PDF downloaded | ⬜ |
| M-009 | Submit article | Article in review queue | ⬜ |
| M-010 | Submit guide listing | Listing pending approval | ⬜ |
| M-011 | Write review | Review submitted | ⬜ |
| M-012 | Take member survey | Response recorded | ⬜ |
| M-013 | Register as volunteer | Volunteer profile created | ⬜ |
| M-014 | View meeting minutes | Public sections visible | ⬜ |
| M-015 | Cancel event registration | Registration cancelled | ⬜ |

### Phase 3: Treasurer Workflow Tests

| Test ID | Test Case | Expected Result | Status |
|---------|-----------|-----------------|--------|
| T-001 | Verify Zelle payment | Payment verified, ledger updated | ⬜ |
| T-002 | Record income transaction | Transaction in ledger | ⬜ |
| T-003 | Record expense transaction | Transaction in ledger | ⬜ |
| T-004 | Approve expense <$500 | Expense approved | ⬜ |
| T-005 | Expense >$500 routes to VP | Approval request sent | ⬜ |
| T-006 | Expense >$1000 routes to Pres | Approval request sent | ⬜ |
| T-007 | Generate monthly report | Report generated | ⬜ |
| T-008 | Export financial data | CSV/Excel downloaded | ⬜ |
| T-009 | View budget vs actual | Comparison displayed | ⬜ |
| T-010 | Record sponsor payment | Payment linked to sponsor | ⬜ |
| T-011 | Process vendor payment | Payment recorded | ⬜ |

### Phase 4: Vice President Workflow Tests

| Test ID | Test Case | Expected Result | Status |
|---------|-----------|-----------------|--------|
| VP-001 | Verify new member | Member activated | ⬜ |
| VP-002 | Create new event | Event published | ⬜ |
| VP-003 | Edit event details | Changes saved | ⬜ |
| VP-004 | View all registrations | List displays | ⬜ |
| VP-005 | Export attendee list | CSV downloaded | ⬜ |
| VP-006 | Approve sponsor (<Gold) | Sponsor activated | ⬜ |
| VP-007 | Review vendor application | Vendor approved | ⬜ |
| VP-008 | Assign volunteer task | Task assigned | ⬜ |
| VP-009 | Respond to complaint | Response sent | ⬜ |
| VP-010 | Publish magazine | Magazine live | ⬜ |
| VP-011 | View financial reports | Reports accessible | ⬜ |

### Phase 5: President Workflow Tests

| Test ID | Test Case | Expected Result | Status |
|---------|-----------|-----------------|--------|
| P-001 | Approve expense >$1000 | Expense processed | ⬜ |
| P-002 | Approve Gold+ sponsor | Sponsor activated | ⬜ |
| P-003 | Suspend member | Member access revoked | ⬜ |
| P-004 | View all admin activity | Audit log displays | ⬜ |
| P-005 | Finalize budget | Budget locked | ⬜ |
| P-006 | Create new admin | Admin access granted | ⬜ |
| P-007 | Modify admin role | Role updated | ⬜ |
| P-008 | Deactivate admin | Access revoked | ⬜ |

### Phase 6: Super Admin Tests

| Test ID | Test Case | Expected Result | Status |
|---------|-----------|-----------------|--------|
| SA-001 | Access system settings | Settings panel opens | ⬜ |
| SA-002 | Modify API configuration | Settings saved | ⬜ |
| SA-003 | View security logs | Logs display | ⬜ |
| SA-004 | Create backup | Backup initiated | ⬜ |
| SA-005 | All permission override | Access to all modules | ⬜ |

---

## 🔧 Backend Services Inventory (42 Modules)

| # | Service File | Purpose | Key Functions |
|---|--------------|---------|---------------|
| 1 | accounting-ledger.jsw | Financial tracking | addFinancialRecord, getFinancialSummary |
| 2 | admin-auth.jsw | Admin authentication | loginAdmin, checkPermission |
| 3 | admin.jsw | Admin operations | getAllAdmins, updateAdminRole |
| 4 | analytics-service.jsw | Site analytics | getPageViews, getUserMetrics |
| 5 | automation-framework.jsw | Task automation | scheduleTask, runWorkflow |
| 6 | budget-finance-service.jsw | Budget management | createEventBudget, trackExpenses |
| 7 | carpool-transport-service.jsw | Transportation | createRide, matchRiders |
| 8 | checkin-kiosk-service.jsw | Event check-in | scanQR, markAttendance |
| 9 | communication-hub.jsw | Messaging | sendBulkEmail, sendSMS |
| 10 | complaints.jsw | Complaint handling | submitComplaint, updateStatus |
| 11 | dashboard-service.jsw | Dashboard data | getStats, getActivityFeed |
| 12 | documents.jsw | Document management | uploadDoc, categorize |
| 13 | email.jsw | Email service | sendEmail, sendTemplate |
| 14 | event-automation.jsw | Event triggers | sendReminders, autoClose |
| 15 | events.jsw | Event CRUD | createEvent, registerForEvent |
| 16 | evite-service.jsw | Digital invitations | createEvite, trackRSVP |
| 17 | feedback-survey-service.jsw | Survey management | createSurvey, submitResponse |
| 18 | finance.jsw | Financial operations | recordTransaction, getBalance |
| 19 | guide.jsw | Jacksonville guide | submitListing, searchPlaces |
| 20 | http-functions.js | API endpoints | GET/POST handlers |
| 21 | magazine.jsw | E-magazine | submitArticle, publishIssue |
| 22 | member-auth.jsw | Member login | memberLogin, sessionManagement |
| 23 | member-automation.jsw | Member triggers | renewalReminders, welcomeEmails |
| 24 | member-directory-service.jsw | Directory | searchMembers, getProfile |
| 25 | members.jsw | Member CRUD | registerMember, updateProfile |
| 26 | payment-automation.jsw | Payment triggers | sendReceipts, overdueAlerts |
| 27 | payment-processing.jsw | Payments | calculateFees, processPayment |
| 28 | photo-gallery-service.jsw | Photo management | uploadPhotos, createAlbum |
| 29 | qr-code-service.jsw | QR generation | generateQR, validateQR |
| 30 | radio-scheduler.jsw | Radio scheduling | createShow, manageSchedule |
| 31 | radio.jsw | Radio streaming | getStatus, submitRequest |
| 32 | sponsor-management.jsw | Sponsors | submitApplication, trackBenefits |
| 33 | sponsorship.jsw | Sponsorship ops | recordPayment, generateReport |
| 34 | streaming-service.jsw | Stream management | startStream, getStats |
| 35 | surveys.jsw | Survey CRUD | createSurvey, getResults |
| 36 | vendor-management.jsw | Vendor management | registerVendor, assignBooth |
| 37 | volunteer-service.jsw | Volunteer ops | registerVolunteer, assignTask |
| **38** | **specialized-admin-roles.jsw** | **Extended admin roles** | **assignSpecializedRole, hasSpecializedPermission** |
| **39** | **reporting-module.jsw** | **Report generation** | **generateReport, scheduleReport, exportReport** |
| **40** | **insights-analytics.jsw** | **Dashboards & KPIs** | **getExecutiveOverview, getPredictiveAnalytics** |
| **41** | **community-engagement.jsw** | **Charity & Programs** | **createInitiative, recordDonation, createScholarship** |
| **42** | **ad-management.jsw** | **Advertising system** | **createCampaign, createAd, recordImpression** |

---

## � Database Collections (New Modules)

### Specialized Admin Roles

| Collection | Purpose | Key Fields |
|------------|---------|------------|
| `SpecializedRoles` | User specialized role assignments | userId, roleId, assignedBy, assignedAt, permissions |

### Reporting Module

| Collection | Purpose | Key Fields |
|------------|---------|------------|
| `ReportHistory` | Generated report archive | reportId, reportType, generatedBy, dateRange, format |
| `ScheduledReports` | Automated report schedules | scheduleId, reportType, frequency, recipients, nextRun |

### Community Engagement Module

| Collection | Purpose | Key Fields |
|------------|---------|------------|
| `CommunityInitiatives` | Charity/community programs | initiativeId, type, title, targetAmount, status |
| `CommunityDonations` | Donation tracking | donationId, initiativeId, donorId, amount, type |
| `CommunityVolunteers` | Volunteer registrations | volunteerId, memberId, skills, availability |
| `VolunteerHours` | Volunteer time tracking | logId, volunteerId, initiativeId, hours, date |
| `CareerGuidanceSessions` | Career program sessions | sessionId, type, mentor, date, capacity |
| `CareerSessionRegistrations` | Session registrations | regId, sessionId, memberId, status |
| `MentorshipMatches` | Mentor-mentee pairings | matchId, mentorId, menteeId, focus, status |
| `Scholarships` | Scholarship programs | scholarshipId, name, amount, criteria, deadline |
| `ScholarshipApplications` | Scholarship applications | appId, scholarshipId, applicantId, documents |
| `CommunityPrograms` | General programs | programId, name, type, startDate, endDate |

### Advertisement Management Module

| Collection | Purpose | Key Fields |
|------------|---------|------------|
| `AdCampaigns` | Advertising campaigns | campaignId, advertiserId, budget, dates, status |
| `Advertisements` | Individual ad units | adId, campaignId, type, placement, creative |
| `AdMetrics` | Performance tracking | metricId, adId, impressions, clicks, conversions |
| `AdInvoices` | Billing records | invoiceId, advertiserId, amount, period, status |

---

## �📱 Responsive Design Requirements

All features must work on:

| Device | Screen Size | Priority |
|--------|-------------|----------|
| Desktop | 1920x1080+ | Primary |
| Laptop | 1366x768 | High |
| Tablet | 768x1024 | High |
| Mobile | 375x667 | Critical |

---

## 🔒 Security Requirements

| Requirement | Implementation |
|-------------|----------------|
| Role-Based Access | Wix Members with custom roles |
| Data Encryption | HTTPS, encrypted at rest |
| Anonymous Submissions | No PII stored |
| Audit Logging | All admin actions tracked |
| Session Management | Auto-timeout after 30min |
| Payment Security | Wix Pay (PCI compliant) |
| API Authentication | Token-based auth |

---

## 📄 Document Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | BANF IT | Initial feature matrix |
| 2.0 | Feb 7, 2026 | BANF IT | Added role hierarchy, approval workflows, comprehensive test cases |
| **3.0** | **Feb 8, 2026** | **BANF IT** | **Added 5 new modules: Specialized Admin Roles (16 roles), Reporting Module (25+ report types), Insights/Analytics Module (8 dashboards), Community Engagement Module (charity, career guidance, scholarships), Ad Management Module (Google Ads-like system). Updated backend services inventory to 42 modules.** |
