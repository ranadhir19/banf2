# BANF Wix Page Setup - Element Reference Guide

## 🎯 Overview

This guide provides the **exact Wix Editor element setup** to match the design in `banf-landing-preview.html`.

**Preview URL:** Open `src/public/banf-landing-preview.html` in browser to see the target design.

---

## 📋 SECTION-BY-SECTION SETUP

---

### 1️⃣ HERO SECTION

**Design:** Full-screen hero with gradient overlay, logo, text, and CTAs

| Element | Wix Type | ID | Content/Settings |
|---------|----------|-----|------------------|
| Section Container | Box | `heroSection` | Full width, min-height 100vh |
| Background Image | Image | - | `https://static.wixstatic.com/media/c62f94_9e58db92918340338d8902f14016a55f~mv2.jpg` |
| Logo Circle | Box + Image | `heroLogo` | White circle with BANF logo |
| Main Title | Heading H1 | `txtEnglishWelcome` | **BANF** (Playfair Display, 4rem, white) |
| Bengali Tagline | Heading H2 | `txtBengaliWelcome` | **বাঙালি এসোসিয়েশন অফ নর্থ ফ্লোরিডা** |
| Location | Paragraph | `txtTagline` | Jacksonville, Florida \| Est. 2008 |
| Join Button | Button | `btnJoinBANF` | "Join Our Community" (White bg, red text) |
| Events Button | Button | `btnExploreEvents` | "Upcoming Events" (Transparent, white border) |

**Colors:**
- Background overlay: `linear-gradient(135deg, rgba(139,0,0,0.9), rgba(255,107,53,0.85), rgba(247,147,30,0.8))`

---

### 2️⃣ STATS STRIP

**Design:** Horizontal gradient strip with 4 stat boxes

| Element | Wix Type | ID | Content |
|---------|----------|-----|---------|
| Section Container | Strip | `statsSection` | Gradient: `linear-gradient(135deg, #8B0000, #ff6b35)` |
| Stat 1 Number | Text | `txtYearsCount` | **17+** |
| Stat 1 Label | Text | `txtYearsLabel` | Years of Heritage |
| Stat 2 Number | Text | `txtMemberCount` | **300+** |
| Stat 2 Label | Text | `txtMemberLabel` | Member Families |
| Stat 3 Number | Text | `txtEventCount` | **50+** |
| Stat 3 Label | Text | `txtEventLabel` | Annual Events |
| Stat 4 Number | Text | `txtSponsorCount` | **1000+** |
| Stat 4 Label | Text | `txtSponsorLabel` | Community Members |

**Styling:** White text, large numbers (3.5rem), Playfair Display font

---

### 3️⃣ PRESIDENT'S MESSAGE SECTION

**Design:** Card with photo header, language toggle, and full message

| Element | Wix Type | ID | Content |
|---------|----------|-----|---------|
| Section Container | Box | `presidentSection` | Background: `#f0f4f8` |
| Section Title Bengali | Text | - | **সভাপতির বার্তা** |
| Section Title English | Text | - | President's Welcome Message |
| President Photo | Image | `imgPresident` | Circle, border, `https://static.wixstatic.com/media/c62f94_rana_ghosh.jpg` |
| President Name | Text | `txtPresidentName` | **Dr. Ranadhir Ghosh** |
| President Title | Text | `txtPresidentTitle` | President, BANF 2025-26 |
| Language Toggle Bengali | Button | `btnLangBengali` | বাংলা |
| Language Toggle English | Button | `btnLangEnglish` | English |
| Bengali Message | Rich Text | `txtMessageBengali` | Full Bengali text (see preview) |
| English Message | Rich Text | `txtMessageEnglish` | Full English text (hidden by default) |

**Special Features:**
- Language toggle switches between Bengali/English versions
- Alert boxes with colored left borders
- Poem section with italics

---

### 4️⃣ EXECUTIVE COMMITTEE SECTION

**Design:** Grid of 8 EC member cards (4 columns on desktop)

| Element | Wix Type | ID | Notes |
|---------|----------|-----|-------|
| Section Container | Box | `leadershipSection` | White background |
| Section Title | Heading | - | **Executive Committee** |
| Section Subtitle | Text | - | 2025-26 Leadership \| 8 Positions |
| EC Repeater | Repeater | `repeaterEC` | 4 columns, 8 items |

**Inside Each Repeater Item:**

| Element | Wix Type | ID | Content |
|---------|----------|-----|---------|
| Member Photo | Image | `imgECMember` | Circle, 100px, orange border |
| Avatar Fallback | Text | `txtECAvatar` | Initials (shown if image fails) |
| Position Badge | Text | `txtECPosition` | e.g., "President" (gradient bg, white text) |
| Member Name | Text | `txtECName` | e.g., "Dr. Ranadhir Ghosh" |
| Role | Text | `txtECRole` | e.g., "Strategic Planning" |
| Bio | Text | `txtECBio` | Short description |

**EC Members (2025-26):**

| # | Position | Name | Photo URL | Email |
|---|----------|------|-----------|-------|
| 1 | President | Dr. Ranadhir Ghosh | `c62f94_rana.jpg` ✅ | president@jaxbengali.org |
| 2 | Vice President | Partha Mukhopadhyay | Upload needed | vp@jaxbengali.org |
| 3 | Treasurer | Amit Chandak | Upload needed | treasurer@jaxbengali.org |
| 4 | General Secretary | Rajanya Ghosh | Upload needed | secretary@jaxbengali.org |
| 5 | Cultural Secretary | Dr. Moumita Ghosh | Upload needed | cultural@jaxbengali.org |
| 6 | Food Coordinator | Banty Dutta | Upload needed | food@jaxbengali.org |
| 7 | Event Coordinator | Dr. Sumanta Ghosh | Upload needed | events@jaxbengali.org |
| 8 | Puja Coordinator | Rwiti Choudhury | Upload needed | puja@jaxbengali.org |

**Note:** EC member photos need to be uploaded to Wix Media Manager and URLs updated

---

### 5️⃣ EVENTS SECTION

**Design:** Event calendar image + 3 event cards

| Element | Wix Type | ID | Content |
|---------|----------|-----|---------|
| Section Container | Box | `eventsSection` | Background: `#f0f4f8` |
| Section Title | Heading | `txtEventsTitle` | **2025 Event Calendar** |
| Calendar Image | Image | `imgEventCalendar` | `c62f94_6f4f1564e4dd4551926fe6cbe715a244~mv2.jpg` |
| Events Repeater | Repeater | `repeaterEvents` | 3 columns |

**Inside Each Event Card:**

| Element | Wix Type | ID | Content |
|---------|----------|-----|---------|
| Event Icon | Icon | `iconEvent` | Font Awesome icon |
| Event Name | Text | `txtEventName` | e.g., "Durga Puja 2025" |
| Event Description | Text | `txtEventDesc` | Short description |
| Event Date Badge | Text | `txtEventDate` | e.g., "October 2025" |
| Details Button | Button | `btnEventDetails` | "View Details" |

**Featured Events:**
1. 🕉️ Durga Puja 2025 - October 2025
2. 📚 Saraswati Puja - February 2025
3. ☀️ Pohela Boishakh - April 2025

---

### 6️⃣ MEMBERSHIP SECTION

**Design:** Dark background with 3 membership cards + 4 sponsorship tiers

| Element | Wix Type | ID | Content |
|---------|----------|-----|---------|
| Section Container | Box | `membershipSection` | Background: `linear-gradient(135deg, #1a1a2e, #16213e)` |
| Section Title | Heading | `txtMembershipTitle` | **Membership & Sponsorship** |
| Membership Repeater | Repeater | `repeaterMembership` | 3 columns |

**Membership Tiers:**

| Type | Price | Features |
|------|-------|----------|
| Individual | $50/year | Single adult, voting rights, newsletter |
| **Family (Featured)** | $100/year | 2 adults + 2 kids, priority registration |
| Senior | $35/year | Age 65+, special seating |

**Sponsorship Tiers:**

| Tier | Price | Color |
|------|-------|-------|
| Platinum | $2,500 | Purple gradient |
| Gold | $1,000 | Gold gradient |
| Silver | $500 | Gray gradient |
| Bronze | $250 | Bronze gradient |

---

### 7️⃣ CONTACT SECTION

**Design:** 3 contact cards + quick contact form

| Element | Wix Type | ID | Content |
|---------|----------|-----|---------|
| Section Container | Box | `contactSection` | Background: `#f8f9fa` |
| Section Title | Heading | `txtContactTitle` | **Contact Us** |
| Contact Repeater | Repeater | - | 3 columns |

**Contact Cards:**

| Type | Icon | Info |
|------|------|------|
| Email | ✉️ | info@jaxbengali.org |
| Website | 🌐 | www.jaxbengali.org |
| Facebook | 📘 | @BengaliAssociationNorthFlorida |

**Contact Form (Optional):**

| Element | Wix Type | ID |
|---------|----------|-----|
| Name Input | Text Input | `inputContactName` |
| Email Input | Text Input | `inputContactEmail` |
| Message Input | Text Box | `inputContactMessage` |
| Submit Button | Button | `btnSubmitQuickContact` |

---

### 8️⃣ FOOTER

**Design:** Dark footer with 4 columns

| Element | Wix Type | ID | Content |
|---------|----------|-----|---------|
| Footer Container | Box | `footerSection` | Background: `linear-gradient(135deg, #1a1a2e, #16213e)` |
| Brand Logo | Text | - | **BANF** with Om icon |
| About Text | Text | `txtFooterAbout` | BANF description |
| Quick Links | Menu | - | President's Message, Leadership, Events, Membership |
| Resources Links | Menu | - | Gallery, Video Archive, Magazine, News |
| Contact Info | Text | `txtFooterContact` | Jacksonville, FL \| info@jaxbengali.org |
| Social Icons | Icons | `socialLinks` | Facebook, Instagram, YouTube, Email |
| Copyright | Text | `txtCopyright` | © 2025 BANF. All rights reserved. |

---

## 🎨 COLOR REFERENCE

| Name | Hex | Usage |
|------|-----|-------|
| Deep Red | `#8B0000` | Primary headers, accents |
| BANF Orange | `#ff6b35` | Buttons, highlights |
| Golden | `#f7931e` | Badges, special elements |
| Bangladesh Green | `#006A4E` | Senior tier, nature themes |
| Dark Navy | `#1a1a2e` | Footer, dark sections |
| Light Gray | `#f0f4f8` | Section backgrounds |

**Gradient Primary:** `linear-gradient(135deg, #8B0000, #ff6b35, #f7931e)`

---

## 📝 FONTS

| Font | Usage |
|------|-------|
| Playfair Display | Headings, brand name, stat numbers |
| Poppins | Body text, buttons, navigation |
| Noto Sans Bengali | Bengali text (বাংলা) |

---

## 🖼️ IMAGE URLs

| Image | URL |
|-------|-----|
| Hero Background | `https://static.wixstatic.com/media/c62f94_9e58db92918340338d8902f14016a55f~mv2.jpg` |
| BANF Logo | `https://static.wixstatic.com/media/c62f94_e8b7a6b7e4834f4db1f1a5d02e7a9a3c~mv2.png` |
| Event Calendar | `https://static.wixstatic.com/media/c62f94_6f4f1564e4dd4551926fe6cbe715a244~mv2.jpg` |
| President Photo | `https://static.wixstatic.com/media/c62f94_rana_ghosh.jpg` |

---

## ⚡ QUICK SETUP STEPS

1. **Open Wix Editor** → Login → Select banf1 site → Edit Site
2. **Enable Dev Mode** → Top menu → Dev Mode ON
3. **Pull from GitHub** → Code Panel → Source Control → Pull
4. **Go to Home Page** → Pages panel → Home
5. **Add Sections** one by one following this guide
6. **Set Element IDs** → Right-click → View Properties → Set ID
7. **Preview** → Test all sections
8. **Publish** when ready

---

## 📁 FILES REFERENCE

| File | Purpose |
|------|---------|
| `src/public/banf-landing-preview.html` | Visual preview (open in browser) |
| `src/pages/Home.js` | Wix page logic (907 lines) |
| `src/pages/masterPage.js` | Global navigation (187 lines) |
| `src/backend/*.jsw` | 41 backend service modules |

---

**Last Updated:** February 8, 2026
