# BANF Dashboard Service Integration Map

## Overview

This document maps all BANF backend services to the appropriate dashboard views based on user roles.

---

## Role Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                         ADMIN                                    │
│  Full access to all services + system settings                  │
├─────────────────────────────────────────────────────────────────┤
│                       EC MEMBER                                  │
│  Access to admin operational services (no settings/audit)       │
├─────────────────────────────────────────────────────────────────┤
│                        MEMBER                                    │
│  Access to personal services only                               │
├─────────────────────────────────────────────────────────────────┤
│                         GUEST                                    │
│  Public view only                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Admin Dashboard Services (10 Categories)

### 1. 📅 Event Management
**Route:** `/admin/events`
**Backend Service:** `evite-service.jsw`

| Function | Description | Access |
|----------|-------------|--------|
| `createEvent()` | Create new event | Admin/EC |
| `updateEvent()` | Modify event details | Admin/EC |
| `deleteEvent()` | Remove event | Admin |
| `getEventRSVPs()` | View all RSVPs | Admin/EC |
| `sendEventReminders()` | Send reminders | Admin/EC |
| `exportAttendeeList()` | Export to Excel | Admin/EC |

### 2. 👥 Member Management
**Route:** `/admin/members`
**Backend Service:** `member-directory-service.jsw`

| Function | Description | Access |
|----------|-------------|--------|
| `getAllMembers()` | List all members | Admin/EC |
| `approveMember()` | Approve membership | Admin |
| `suspendMember()` | Suspend account | Admin |
| `assignRole()` | Assign roles | Admin |
| `exportMembers()` | Export member data | Admin |

### 3. 💰 Financial Management
**Route:** `/admin/finance`
**Backend Service:** `budget-finance-service.jsw`

| Function | Description | Access |
|----------|-------------|--------|
| `createBudget()` | Create annual budget | Admin |
| `recordExpense()` | Record expense | Admin/EC |
| `recordIncome()` | Record income | Admin/EC |
| `approveExpense()` | Approve expenses | Admin |
| `generateFinancialReport()` | Generate reports | Admin/EC |
| `getFinancialSummary()` | Dashboard summary | Admin/EC |

### 4. 📢 Communication Hub
**Route:** `/admin/communications`
**Backend Service:** `communication-hub.jsw`

| Function | Description | Access |
|----------|-------------|--------|
| `sendAnnouncement()` | Send to all members | Admin/EC |
| `sendSMSNotification()` | SMS blast | Admin |
| `sendPushNotification()` | Push notifications | Admin/EC |
| `scheduleMessage()` | Schedule future message | Admin/EC |
| `getMessageHistory()` | View sent messages | Admin/EC |

### 5. 📊 Analytics & Insights
**Route:** `/admin/analytics`
**Backend Service:** `analytics-service.jsw`

| Function | Description | Access |
|----------|-------------|--------|
| `getEventAnalytics()` | Event metrics | Admin/EC |
| `getMembershipAnalytics()` | Member trends | Admin/EC |
| `getFinancialAnalytics()` | Financial charts | Admin |
| `getEngagementMetrics()` | Engagement stats | Admin/EC |
| `generateCustomReport()` | Custom reports | Admin/EC |

### 6. 🏢 Vendors & Sponsors
**Route:** `/admin/vendors`
**Backend Service:** `vendor-sponsor-service.jsw` (to be created)

| Function | Description | Access |
|----------|-------------|--------|
| `addVendor()` | Add vendor | Admin |
| `addSponsor()` | Add sponsor | Admin |
| `trackPayments()` | Track vendor payments | Admin |
| `manageSponsorLevels()` | Sponsor tier management | Admin |

### 7. 🛡️ Content Moderation
**Route:** `/admin/moderation`
**Backend Service:** `photo-gallery-service.jsw`, `feedback-survey-service.jsw`

| Function | Description | Access |
|----------|-------------|--------|
| `getPendingPhotos()` | Photos awaiting approval | Admin/EC |
| `moderatePhoto()` | Approve/reject photo | Admin/EC |
| `reviewFeedback()` | Review survey responses | Admin/EC |
| `flagContent()` | Flag inappropriate content | Admin/EC |

### 8. 🤝 Volunteer Coordination
**Route:** `/admin/volunteers`
**Backend Service:** `volunteer-service.jsw`

| Function | Description | Access |
|----------|-------------|--------|
| `createVolunteerOpportunity()` | Create opportunity | Admin/EC |
| `assignVolunteers()` | Assign to tasks | Admin/EC |
| `approveVolunteerHours()` | Approve hours | Admin/EC |
| `getVolunteerLeaderboard()` | Recognition stats | Admin/EC |
| `exportVolunteerReport()` | Export hours | Admin/EC |

### 9. ✅ Check-in Operations
**Route:** `/admin/checkin`
**Backend Service:** `qr-code-service.jsw`, `checkin-kiosk-service.jsw`

| Function | Description | Access |
|----------|-------------|--------|
| `generateEventQRCodes()` | Bulk QR generation | Admin/EC |
| `initializeKiosk()` | Setup kiosk | Admin |
| `getCheckInStats()` | Real-time check-in | Admin/EC |
| `validateQRCode()` | Manual validation | Admin/EC |
| `printBadge()` | Print name badge | Admin/EC |

### 10. 🎵 Streaming & Radio
**Route:** `/admin/radio`
**Backend Service:** `streaming-service.jsw` (to be created)

| Function | Description | Access |
|----------|-------------|--------|
| `startStream()` | Start live stream | Admin |
| `managePlaylist()` | Manage radio playlist | Admin/EC |
| `schedulePrograms()` | Schedule shows | Admin/EC |
| `getListenerStats()` | Streaming analytics | Admin/EC |

---

## Member Dashboard Services (8 Categories)

### 1. 👤 My Profile
**Route:** `/member/profile`
**Backend Service:** `member-directory-service.jsw`

| Function | Description |
|----------|-------------|
| `getMemberProfile()` | View own profile |
| `updateProfile()` | Edit profile info |
| `uploadAvatar()` | Change profile photo |
| `updatePreferences()` | Notification preferences |
| `changePassword()` | Security settings |

### 2. 📅 My Events
**Route:** `/member/events`
**Backend Service:** `evite-service.jsw`

| Function | Description |
|----------|-------------|
| `getUpcomingEvents()` | Browse events |
| `rsvpToEvent()` | RSVP to event |
| `cancelRSVP()` | Cancel RSVP |
| `getMyRSVPs()` | View my RSVPs |
| `addToCalendar()` | Calendar integration |

### 3. 🎫 My Membership
**Route:** `/member/membership`
**Backend Service:** `membership-service.jsw`

| Function | Description |
|----------|-------------|
| `getMembershipStatus()` | View status |
| `renewMembership()` | Renew online |
| `getPaymentHistory()` | Payment records |
| `downloadMemberCard()` | Digital card |

### 4. 📇 Member Directory
**Route:** `/member/directory`
**Backend Service:** `member-directory-service.jsw`

| Function | Description |
|----------|-------------|
| `searchMembers()` | Search directory |
| `getMemberProfile()` | View profiles |
| `requestConnection()` | Connect request |
| `getConnections()` | My connections |
| `messageConnection()` | Direct message |

### 5. 📸 Photo Gallery
**Route:** `/member/photos`
**Backend Service:** `photo-gallery-service.jsw`

| Function | Description |
|----------|-------------|
| `getEventPhotos()` | Browse photos |
| `uploadPhoto()` | Upload photos |
| `getTaggedPhotos()` | Photos I'm in |
| `tagMember()` | Tag people |
| `downloadPhoto()` | Download photos |

### 6. 🚗 Carpool
**Route:** `/member/carpool`
**Backend Service:** `carpool-transport-service.jsw`

| Function | Description |
|----------|-------------|
| `offerRide()` | Offer a ride |
| `requestRide()` | Request ride |
| `matchRides()` | Find matches |
| `confirmRide()` | Confirm booking |
| `getRideHistory()` | Past rides |

### 7. 💪 Volunteer
**Route:** `/member/volunteer`
**Backend Service:** `volunteer-service.jsw`

| Function | Description |
|----------|-------------|
| `getOpportunities()` | View opportunities |
| `signUpVolunteer()` | Sign up |
| `getVolunteerHours()` | My hours log |
| `getVolunteerRank()` | Leaderboard rank |

### 8. 💬 Feedback
**Route:** `/member/feedback`
**Backend Service:** `feedback-survey-service.jsw`

| Function | Description |
|----------|-------------|
| `getPendingSurveys()` | Pending surveys |
| `submitFeedback()` | Complete survey |
| `submitSuggestion()` | Submit idea |

---

## Service Integration Architecture

```
                    ┌─────────────────────────────────────┐
                    │         BANF Web Platform           │
                    └─────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
            ┌───────▼───────┐ ┌─────▼─────┐ ┌──────▼──────┐
            │ Admin Dashboard│ │ Member    │ │ Public      │
            │ (10 Categories)│ │ Dashboard │ │ Pages       │
            │               │ │(8 Services)│ │ (Limited)   │
            └───────┬───────┘ └─────┬─────┘ └──────┬──────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │    Dashboard Router            │
                    │  (public/dashboard-router.js)  │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │    Service Controller          │
                    │(public/service-controller.js)  │
                    └───────────────┬───────────────┘
                                    │
        ┌───────────┬───────────┬───┴───┬───────────┬───────────┐
        │           │           │       │           │           │
┌───────▼───┐ ┌─────▼─────┐ ┌───▼───┐ ┌─▼─┐ ┌───────▼───┐ ┌─────▼─────┐
│ evite     │ │ qr-code   │ │volun- │ │...│ │ member-   │ │ feedback  │
│ service   │ │ service   │ │teer   │ │   │ │ directory │ │ survey    │
└───────────┘ └───────────┘ └───────┘ └───┘ └───────────┘ └───────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │     dashboard-service.jsw      │
                    │  (Role Detection & Routing)    │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │         Wix Data API           │
                    │    (CMS Collections)           │
                    └────────────────────────────────┘
```

---

## Files Created

### Backend Services (Velo Backend)
| File | Purpose |
|------|---------|
| `dashboard-service.jsw` | Role detection, categorization, unified dashboard data |
| `evite-service.jsw` | Event management & RSVPs |
| `qr-code-service.jsw` | QR generation & validation |
| `analytics-service.jsw` | Reporting & metrics |
| `volunteer-service.jsw` | Volunteer management |
| `communication-hub.jsw` | Announcements & notifications |
| `checkin-kiosk-service.jsw` | Self-service check-in |
| `budget-finance-service.jsw` | Financial tracking |
| `photo-gallery-service.jsw` | Photo management |
| `feedback-survey-service.jsw` | Surveys & feedback |
| `carpool-transport-service.jsw` | Ride sharing |
| `member-directory-service.jsw` | Member search & profiles |

### Frontend Modules (Velo Frontend)
| File | Purpose |
|------|---------|
| `dashboard-router.js` | Role-based navigation |
| `service-controller.js` | Unified service interface |

### Page Code
| File | Purpose |
|------|---------|
| `admin-dashboard.js` | Admin dashboard page logic |
| `member-dashboard.js` | Member dashboard page logic |

### HTML Templates
| File | Purpose |
|------|---------|
| `admin-dashboard.html` | Admin UI template |
| `member-dashboard.html` | Member UI template |

---

## Implementation Checklist

### Phase 1: Core Setup ✅
- [x] Create dashboard-service.jsw with role detection
- [x] Create dashboard-router.js for navigation
- [x] Create service-controller.js for unified API
- [x] Create admin-dashboard.html template
- [x] Create member-dashboard.html template
- [x] Create page code for both dashboards

### Phase 2: Wix Studio Integration
- [ ] Create Admin Dashboard page in Wix Editor
- [ ] Create Member Dashboard page in Wix Editor
- [ ] Add all UI elements with matching IDs
- [ ] Connect repeaters to data sources
- [ ] Create required lightboxes
- [ ] Setup page permissions (Admin page: admin only)

### Phase 3: Testing
- [ ] Test admin role detection
- [ ] Test EC member role detection
- [ ] Test member access restrictions
- [ ] Test guest redirect to login
- [ ] Test all service endpoints
- [ ] Test navigation between services

### Phase 4: Deployment
- [ ] Deploy to staging site
- [ ] User acceptance testing
- [ ] Deploy to production
- [ ] Monitor for issues

---

## Kolkata Theme Colors Reference

```css
/* Primary BANF Colors */
--banf-saffron: #ff6b35;
--banf-orange: #f7931e;
--banf-yellow: #f5af19;

/* Accent Colors */
--banf-deep-red: #8B0000;
--banf-burgundy: #722f37;
--banf-green: #006A4E;
--banf-gold: #daa520;

/* Gradients */
--gradient-primary: linear-gradient(135deg, #ff6b35 0%, #f5af19 100%);
--gradient-secondary: linear-gradient(135deg, #8B0000 0%, #722f37 100%);
--gradient-success: linear-gradient(135deg, #006A4E 0%, #28a745 100%);
```

---

## Summary

| Category | Admin Services | Member Services |
|----------|---------------|-----------------|
| Events | Create, Manage, RSVPs, Reminders | Browse, RSVP, Cancel |
| Members | Full CRUD, Roles, Export | Profile, Directory, Connect |
| Finance | Budget, Expenses, Reports | View Payment History |
| Communication | Announcements, SMS, Push | Receive Notifications |
| Analytics | Full Reports | N/A |
| Photos | Moderation | Upload, View, Tag |
| Volunteers | Manage, Approve Hours | Sign Up, Track Hours |
| Check-in | Kiosk, QR Validation | View Own QR |
| Carpool | N/A | Offer/Request Rides |
| Feedback | Review Responses | Submit Surveys |

**Total Backend Modules:** 18
**Admin Service Categories:** 10
**Member Service Categories:** 8
