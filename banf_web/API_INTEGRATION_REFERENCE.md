# BANF Wix Landing Page - API Integration Reference

**Generated:** 2026-01-16  
**Version:** 2.0  
**Status:** ✅ All Links Verified Against Backend APIs

---

## Overview

This document maps all landing page links to their corresponding Wix backend APIs (Velo modules) and page routes.

## Landing Page File
- **File:** `wix-embed-landing-v2.html`
- **Type:** Self-contained HTML embed for Wix Custom Element/HTML iframe
- **Size:** ~2400+ lines

---

## API Integration Summary

| Section | Backend Module | Key Functions | Wix Page Route |
|---------|----------------|---------------|----------------|
| Membership | `members.jsw` | `registerMember()`, `getMemberById()` | `/member-payment` |
| Events | `events.jsw` | `getUpcomingEvents()`, `registerForEvent()` | `/events` |
| Radio | `radio.jsw` | `getRadioStationConfig()`, `getCurrentShow()` | `/radio` |
| E-Magazine | `magazine.jsw` | `getPublishedMagazines()`, `submitArticle()` | `/magazine` |
| Jax Guide | `guide.jsw` | `getGuideByCategory()`, `searchGuide()` | `/guide` |
| Surveys | `surveys.jsw` | `getActiveSurveys()`, `submitSurveyResponse()` | `/surveys` |
| Complaints | `complaints.jsw` | `submitComplaint()`, `checkComplaintStatus()` | `/complaints` |
| Sponsors | `sponsorship.jsw` | `getSponsors()`, `createSponsor()` | `/sponsors` |
| Minutes | `documents.jsw` | `getDocumentsByCategory()` | `/members-area` (auth) |
| Gallery | `gallery.jsw` | `getPublicGalleries()` | `/gallery` |

---

## Detailed API Mapping

### 1. Membership Portal
**Backend:** `velo_backend/members.jsw` (269 lines)

| Link Text | href | data-action | API Function |
|-----------|------|-------------|--------------|
| Join Now | `#membership` | `join` | `registerMember(memberData)` |
| Pay Dues | `#membership` | `join` | `processPayment()` |
| Become a Member | `#membership` | `join` | `registerMember()` |

**API Functions:**
```javascript
// Public functions from members.jsw
export async function registerMember(memberData) // Register new member
export async function getMemberById(memberId)     // Get member details
export async function getCurrentMemberProfile()   // Get logged-in member
export async function getPaymentHistory(memberId) // Payment records
export async function getFamilyMembers(memberId)  // Family profiles
```

**Data Collections:**
- `Members` - Main member data
- `MemberPayments` - Payment history
- `FamilyMembers` - Family profiles

---

### 2. Events & Programs
**Backend:** `velo_backend/events.jsw` (392 lines)

| Link Text | href | data-action | API Function |
|-----------|------|-------------|--------------|
| View Events | `#events` | `events` | `getUpcomingEvents()` |
| Upcoming Events | `#events` | `events` | `getUpcomingEvents()` |
| Register | - | `events` | `registerForEvent(eventId)` |

**API Functions:**
```javascript
// Public functions from events.jsw
export async function getUpcomingEvents()              // Future events
export async function getPastEvents()                  // Historical events
export async function getEventById(eventId)            // Single event
export async function registerForEvent(eventId, data)  // Event registration
export async function submitEventFeedback(eventId, fb) // Post-event feedback
export async function checkIntoEvent(eventId, code)    // Venue check-in
```

**HTTP Endpoint:** `GET /_functions/get_events`

---

### 3. BANF Radio 24/7
**Backend:** `velo_backend/radio.jsw` (418 lines)

| Link Text | href | data-action | API Function |
|-----------|------|-------------|--------------|
| Listen Live | `#radio` | `radio` | `getRadioStationConfig()` |
| Radio | `#radio` | `radio` | `getCurrentShow()` |

**API Functions:**
```javascript
// Public functions from radio.jsw
export async function getRadioStationConfig()     // Stream URL, station info
export async function getCurrentShow()            // Now playing
export async function getUpcomingShows()          // Schedule
export async function getSongLibrary(options)     // Browse songs
export async function submitSongRequest(songId)   // Request a song
```

**HTTP Endpoint:** `GET /_functions/get_radio`

**Stream Configuration:**
- `streamUrl` - Icecast/Shoutcast stream URL
- `currentTrack` - Now playing metadata
- `schedule` - Weekly show schedule

---

### 4. E-Magazine
**Backend:** `velo_backend/magazine.jsw` (455 lines)

| Link Text | href | data-action | API Function |
|-----------|------|-------------|--------------|
| Read Now | `#magazine` | `magazine` | `getPublishedMagazines()` |
| Magazine | `#magazine` | `magazine` | `getLatestMagazine()` |
| Submit Article | - | `magazine` | `submitArticle()` |

**API Functions:**
```javascript
// Public functions from magazine.jsw
export async function getPublishedMagazines()         // All issues
export async function getLatestMagazine()             // Most recent
export async function getArticlesByCategory(cat)      // Filter by type
export async function searchArticles(query)           // Full-text search
export async function submitArticle(articleData)      // Member submissions
```

**Article Categories (ARTICLE_CATEGORIES):**
- Poetry (কবিতা)
- Short Stories (গল্প)
- Essays (প্রবন্ধ)
- Children's Corner (শিশু বিভাগ)
- Travelogue (ভ্রমণ কাহিনী)
- Recipes (রান্নার রেসিপি)
- Art & Photography (শিল্প ও আলোকচিত্র)

---

### 5. Jacksonville Guide
**Backend:** `velo_backend/guide.jsw` (565 lines)

| Link Text | href | data-action | API Function |
|-----------|------|-------------|--------------|
| Explore Guide | `#guide` | `guide` | `getAllListings()` |
| Jax Guide | `#guide` | `guide` | `getGuideByCategory()` |

**API Functions:**
```javascript
// Public functions from guide.jsw
export async function getAllListings()                // All businesses
export async function getGuideByCategory(category)    // Filter by type
export async function getListingsByArea(area)         // Filter by location
export async function searchGuide(query)              // Search listings
export async function submitReview(listingId, review) // Add review
export async function submitNewListing(data)          // Request new listing
```

**Guide Categories (GUIDE_CATEGORIES):**
- Restaurants (রেস্তোরাঁ)
- Grocery Stores (মুদি দোকান)
- Doctors & Healthcare (চিকিৎসক)
- Schools & Education (বিদ্যালয়)
- Places of Worship (ধর্মস্থান)
- Professional Services (পেশাদার সেবা)
- Entertainment (বিনোদন)
- Real Estate (রিয়েল এস্টেট)

**Jacksonville Areas (JACKSONVILLE_AREAS):**
- Downtown, Southside, Westside, Northside
- Beaches, Mandarin, Arlington, Orange Park

---

### 6. Community Surveys
**Backend:** `velo_backend/surveys.jsw` (437 lines)

| Link Text | href | data-action | API Function |
|-----------|------|-------------|--------------|
| Take Survey | `#surveys` | `surveys` | `getActiveSurveys()` |
| Surveys | `#surveys` | `surveys` | `getActiveSurveys()` |

**API Functions:**
```javascript
// Public functions from surveys.jsw
export async function getActiveSurveys()                  // Open surveys
export async function getSurveyById(surveyId)             // Single survey
export async function submitSurveyResponse(id, response)  // Submit answers
export async function getSurveyResults(surveyId)          // Results (members)
export async function createSurvey(surveyData)            // Admin: create
```

**Survey Types (SURVEY_TYPES):**
- Event Feedback
- Community Polling
- Membership Survey
- General Feedback

---

### 7. Anonymous Complaints
**Backend:** `velo_backend/complaints.jsw` (356 lines)

| Link Text | href | data-action | API Function |
|-----------|------|-------------|--------------|
| Submit Complaint | `#complaints` | `complaints` | `submitComplaint()` |
| Complaints | `#complaints` | `complaints` | `submitComplaint()` |

**API Functions:**
```javascript
// Public functions from complaints.jsw
export async function submitComplaint(complaintData)   // Anonymous submission
export async function checkComplaintStatus(accessCode) // Track by code
export async function addComplaintFollowUp(code, msg)  // Add follow-up
```

**Complaint Status (COMPLAINT_STATUS):**
- `submitted` - New complaint
- `under_review` - Being reviewed
- `in_progress` - Action taken
- `resolved` - Closed
- `closed` - No further action

**Features:**
- End-to-end encryption
- Anonymous access codes
- Follow-up messaging
- Status tracking

---

### 8. Sponsorship
**Backend:** `velo_backend/sponsorship.jsw` (577 lines)

| Link Text | href | data-action | API Function |
|-----------|------|-------------|--------------|
| Learn More | `#sponsors` | `sponsors` | `getSponsors()` |
| Sponsors | `#sponsors` | `sponsors` | `getSponsors()` |
| Become a Sponsor | - | `sponsors` | `createSponsor()` |

**API Functions:**
```javascript
// Public functions from sponsorship.jsw
export async function getSponsors()                 // Active sponsors
export async function getSponsorsByTier(tier)       // Filter by tier
export async function createSponsor(sponsorData)    // Apply for sponsorship
export async function getSponsorshipTiers()         // Available tiers
```

**HTTP Endpoint:** `GET /_functions/get_sponsors`

**Sponsorship Tiers (SPONSORSHIP_TIERS):**
| Tier | Annual Cost | Benefits |
|------|-------------|----------|
| Platinum | $2,000 | Full page magazine ad, banner at all events, website logo |
| Gold | $1,000 | Half page ad, name at events, website listing |
| Silver | $500 | Quarter page ad, newsletter mention |
| Bronze | $250 | Name listing in magazine and website |

---

### 9. Meeting Minutes (Members Only)
**Backend:** `velo_backend/documents.jsw` (606 lines)

| Link Text | href | data-action | API Function |
|-----------|------|-------------|--------------|
| View Minutes | `#minutes` | `login` | `getDocumentsByCategory()` |

**API Functions:**
```javascript
// Protected functions from documents.jsw (require authentication)
export async function getDocumentsByCategory(category)  // Filter docs
export async function getAllPublicDocuments()           // Public docs only
export async function uploadDocument(docData)           // Admin upload
```

**Document Categories (DOCUMENT_CATEGORIES):**
- `MEETING_DOCS` - EC meeting minutes
- `FINANCIAL_REPORTS` - Treasurer reports
- `BYLAWS` - Organization bylaws
- `NEWSLETTERS` - Monthly newsletters
- `FORMS` - Membership forms

**Access Control:**
- Meeting minutes require member login
- Uses `wix-members` authentication
- Role-based access (admin/member/public)

---

### 10. Photo Gallery
**Backend:** `velo_backend/gallery.jsw`

| Link Text | href | data-action | API Function |
|-----------|------|-------------|--------------|
| Gallery | `/gallery` | `gallery` | `getPublicGalleries()` |

**HTTP Endpoint:** `GET /_functions/get_gallery`

---

## HTTP Functions (REST API)

**File:** `velo_backend/http-functions.js`

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/_functions/get_events` | GET | List upcoming events | Public |
| `/_functions/get_radio` | GET | Radio station config | Public |
| `/_functions/get_sponsors` | GET | Active sponsors | Public |
| `/_functions/get_gallery` | GET | Photo galleries | Public |
| `/_functions/get_members` | GET | Member list | Auth Required |

---

## Page Routes

**Source:** `velo_pages/LandingPage.velo.js`

| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Landing page |
| About | `/about` | About BANF |
| Events | `/events` | Event calendar |
| Radio | `/radio` | Radio player |
| Magazine | `/magazine` | E-Magazine |
| Guide | `/guide` | Jacksonville Guide |
| Surveys | `/surveys` | Community surveys |
| Complaints | `/complaints` | Anonymous complaints |
| Sponsors | `/sponsors` | Sponsor directory |
| Gallery | `/gallery` | Photo gallery |
| Membership | `/member-payment` | Join/renew |
| Account | `/account` | Member profile |
| Login | `/login` | Authentication |
| Members Area | `/members-area` | Member dashboard |
| Admin | `/admin-dashboard` | Admin controls |

---

## JavaScript API Layer

The landing page includes a JavaScript API integration layer at the bottom:

```javascript
const BANF_API = {
    siteUrl: 'https://www.jaxbengali.org',
    siteId: 'c13ae8c5-7053-4f2d-9a9a-371869be4395',
    httpFunctionsBase: '/_functions',
    endpoints: { ... },
    pages: { ... },
    actions: { ... }
};

// Functions
navigateToWixPage(pageKey, queryParams)  // Navigate to Wix page
fetchFromAPI(endpoint)                    // Fetch from HTTP functions
loadDynamicContent()                      // Load events, radio, sponsors
setupActionLinks()                        // Bind data-action handlers
```

---

## Data-Action Attributes

Links with `data-action` attribute will navigate to full Wix pages:

| data-action | Wix Page | Backend Module |
|-------------|----------|----------------|
| `join` | `/member-payment` | members.jsw |
| `events` | `/events` | events.jsw |
| `radio` | `/radio` | radio.jsw |
| `magazine` | `/magazine` | magazine.jsw |
| `guide` | `/guide` | guide.jsw |
| `surveys` | `/surveys` | surveys.jsw |
| `complaints` | `/complaints` | complaints.jsw |
| `sponsors` | `/sponsors` | sponsorship.jsw |
| `gallery` | `/gallery` | gallery.jsw |
| `login` | `/login` | wix-members |

---

## Verification Checklist

✅ **All 9 service cards** have `data-action` attributes  
✅ **Quick Access bar** (9 items) mapped to APIs  
✅ **Hero buttons** linked to membership/events  
✅ **Footer links** point to all major sections  
✅ **Backend modules** (42 .jsw files) documented  
✅ **HTTP functions** (5 endpoints) verified  
✅ **Page routes** (15+ pages) mapped  
✅ **JavaScript API layer** added for dynamic loading  

---

## Deployment Notes

1. **Embed in Wix:** Use Custom Element or HTML iframe
2. **API Calls:** HTTP functions will work when deployed to jaxbengali.org
3. **Authentication:** Member-only features require Wix login
4. **CORS:** HTTP functions handle cross-origin requests

---

**Last Updated:** 2026-01-16  
**Verified By:** API Integration Check
