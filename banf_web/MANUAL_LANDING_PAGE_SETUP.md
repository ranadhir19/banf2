# BANF Landing Page - Manual Setup Guide

## 📋 Overview
This guide walks you through manually setting up the BANF landing page in Wix Editor with all backend integrations.

---

## 🔐 Step 1: Login to Wix

1. Go to: https://manage.wix.com
2. Login with:
   - **Email:** `Banfjax@gmail.com`
   - **Password:** `Banfec2022`
3. Select your **banf1** (DEV) site
4. Click **"Edit Site"** to open the Editor

---

## 🔧 Step 2: Enable Dev Mode

1. In the Editor, look at the **top menu bar**
2. Find **"Dev Mode"** toggle (usually top-left area)
3. Click to **turn it ON**
4. You should see a **Code Panel** appear on the left sidebar

---

## 🔄 Step 3: Pull GitHub Changes

1. In the **Code Panel** (left sidebar), look for:
   - A **{ }** code icon, or
   - **"Source Control"** section at the bottom
2. Click the **GitHub/Source Control** icon
3. Click **"Pull"** to get latest code from GitHub
4. Wait for sync to complete
5. Verify you see these files in Code Panel:
   - `pages/Home.js` ✅
   - `backend/*.jsw` (36 files) ✅

---

## 🏠 Step 4: Setup Home Page Structure

### Navigate to Home Page
1. In the Editor, click **"Pages"** in left panel
2. Select **"Home"** page
3. Delete any existing content (select all → delete)

---

## 🎨 Step 5: Add Page Elements

### A. HERO SECTION (Top of page)

| # | Element Type | How to Add | Set ID To | Content |
|---|-------------|------------|-----------|---------|
| 1 | **Container Box** | Add → Box | `heroSection` | Full width, green background (#006A4E) |
| 2 | **Text** | Add → Text → Heading | `txtBengaliWelcome` | স্বাগতম |
| 3 | **Text** | Add → Text → Heading | `txtEnglishWelcome` | Welcome to BANF |
| 4 | **Text** | Add → Text → Paragraph | `txtTagline` | Preserving Bengali culture since 1988 |
| 5 | **Button** | Add → Button | `btnJoinBANF` | "Join Our Community" |
| 6 | **Button** | Add → Button | `btnExploreEvents` | "Explore Events" |

**How to set element ID:**
1. Click on element
2. Right-click → **"View Properties"** (or click ⚙️ icon)
3. Find **"ID"** field
4. Type the ID (without #)
5. Press Enter

---

### B. STATS STRIP

| # | Element Type | Set ID To | Content |
|---|-------------|-----------|---------|
| 1 | Container Box | `statsSection` | Horizontal strip |
| 2 | Text | `txtMemberCount` | 500+ |
| 3 | Text | `txtMemberLabel` | Active Members |
| 4 | Text | `txtEventCount` | 50+ |
| 5 | Text | `txtEventLabel` | Events Yearly |
| 6 | Text | `txtYearsCount` | 35+ |
| 7 | Text | `txtYearsLabel` | Years Strong |

---

### C. QUICK ACCESS STRIP (6 icon boxes)

| # | Element Type | Set ID To | Link To | Icon | Label |
|---|-------------|-----------|---------|------|-------|
| 1 | Box/Button | `quickEvents` | /events | 📅 | Events |
| 2 | Box/Button | `quickMembers` | /members | 👥 | Members |
| 3 | Box/Button | `quickRadio` | /radio | 📻 | Radio |
| 4 | Box/Button | `quickMagazine` | /magazine | 📖 | Magazine |
| 5 | Box/Button | `quickGallery` | /gallery | 🖼️ | Gallery |
| 6 | Box/Button | `quickVolunteer` | /volunteer | 🤝 | Volunteer |

**To add links:**
1. Select the box/button
2. Click link icon (🔗)
3. Choose "Page" → select the page

---

### D. FEATURED EVENTS SECTION

| # | Element Type | Set ID To | Notes |
|---|-------------|-----------|-------|
| 1 | Container | `eventsSection` | Section wrapper |
| 2 | Text | `txtEventsTitle` | "Upcoming Events" |
| 3 | **Repeater** | `repeaterEvents` | Add → Lists & Grids → Repeater |

**Configure Repeater:**
1. Add a Repeater (Add → Lists & Grids → Repeater)
2. Set ID to `repeaterEvents`
3. Inside each item, add:
   - Image element → ID: `eventImage`
   - Text → ID: `eventTitle`
   - Text → ID: `eventDate`
   - Text → ID: `eventLocation`
   - Button → ID: `btnEventDetails`

---

### E. RADIO SECTION

| # | Element Type | Set ID To | Content |
|---|-------------|-----------|---------|
| 1 | Container | `radioSection` | Dark background (#1a1a2e) |
| 2 | Text | `txtRadioTitle` | BANF Radio |
| 3 | Text | `txtRadioStatus` | 🔴 LIVE |
| 4 | Text | `txtNowPlaying` | Bengali Music Hour |
| 5 | Button | `btnPlayRadio` | ▶ Play |
| 6 | Button | `btnStopRadio` | ⏹ Stop |

---

### F. MEMBERSHIP CTA SECTION

| # | Element Type | Set ID To | Content |
|---|-------------|-----------|---------|
| 1 | Container | `membershipSection` | Green gradient background |
| 2 | Text | `txtMembershipTitle` | Join the BANF Family |
| 3 | **Repeater** | `repeaterMembership` | Membership tiers |
| 4 | Button | `btnBecomeMember` | "Become a Member" → links to /register |

---

### G. CONTACT FORM SECTION

| # | Element Type | Set ID To | Placeholder |
|---|-------------|-----------|-------------|
| 1 | Container | `contactSection` | - |
| 2 | Text Input | `inputContactName` | Your Name |
| 3 | Text Input | `inputContactEmail` | Your Email |
| 4 | Text Input | `inputContactSubject` | Subject |
| 5 | Text Box | `inputContactMessage` | Your Message |
| 6 | Button | `btnSubmitQuickContact` | Send Message |

---

### H. FOOTER

| # | Element Type | Set ID To | Content |
|---|-------------|-----------|---------|
| 1 | Container | `footerSection` | Dark background |
| 2 | Text | `txtFooterAbout` | BANF description |
| 3 | Text | `txtFooterContact` | Contact info |
| 4 | Text | `txtCopyright` | © 2026 BANF |

---

## 🎨 Step 6: Apply Styling

### Color Scheme (Bangladesh Flag)
| Color | Hex Code | Use For |
|-------|----------|---------|
| Green | `#006A4E` | Primary backgrounds, buttons |
| Red | `#F42A41` | Accents, CTAs |
| Gold | `#FFD700` | Highlights, badges |
| White | `#FFFFFF` | Text on dark backgrounds |
| Dark | `#1a1a2e` | Footer, radio section |

### Typography
- **Headings:** Poppins Bold
- **Bengali Text:** Noto Sans Bengali
- **Body:** Poppins Regular

---

## 🔗 Step 7: Create Required Pages

Make sure these pages exist (Pages panel → + Add Page):

| Page Name | URL | Purpose |
|-----------|-----|---------|
| Home | / | Landing page |
| Events | /events | Event calendar |
| Members | /members | Member directory |
| Radio | /radio | Radio player |
| Magazine | /magazine | প্রতিবিম্ব magazine |
| Gallery | /gallery | Photo gallery |
| Volunteer | /volunteer | Volunteer signup |
| Sponsors | /sponsors | Sponsor showcase |
| Contact | /contact | Contact form |
| Admin | /admin | Admin dashboard |
| Register | /register | Membership signup |

---

## ✅ Step 8: Verify Code Connection

1. Open **Code Panel** (left sidebar)
2. Expand **Pages** → **Home**
3. Click on `Home.js`
4. Verify the code contains:
   - `$w.onReady()` function
   - References to your element IDs
   - Backend imports like `import { getUpcomingEvents } from 'backend/events.jsw'`

---

## 🚀 Step 9: Preview & Test

1. Click **"Preview"** button (top right)
2. Check:
   - [ ] Hero section displays correctly
   - [ ] Stats show numbers (or loading...)
   - [ ] Quick access links work
   - [ ] Events repeater populates
   - [ ] Radio section shows status
   - [ ] Contact form submits
3. Open browser console (F12) to check for errors

---

## 📤 Step 10: Publish

1. Click **"Publish"** button (top right)
2. Confirm publish
3. Visit your live site URL to verify

---

## 🆘 Troubleshooting

### "Element not found" errors
- Check element ID matches exactly (case-sensitive)
- Make sure you removed the `#` when setting ID in Wix

### Code not running
- Ensure Dev Mode is ON
- Check that `Home.js` exists in Code Panel

### Repeater not populating
- Check backend connection in Code Panel
- Verify database collections exist

### Styles not applying
- The Home.js includes dynamic styling
- Check if elements have correct IDs

---

## 📁 Reference Files

| File | Location | Purpose |
|------|----------|---------|
| Home.js | `wix-github-repo/src/pages/Home.js` | All homepage logic |
| Home.html | `wix-github-repo/src/pages/Home.html` | Design reference |
| Backend files | `wix-github-repo/src/backend/*.jsw` | 36 service modules |

---

## 🎯 Quick Checklist

- [ ] Logged into Wix
- [ ] Dev Mode enabled
- [ ] GitHub changes pulled
- [ ] Hero section added with IDs
- [ ] Stats strip added with IDs
- [ ] Quick access buttons with links
- [ ] Events repeater configured
- [ ] Radio section added
- [ ] Membership section added
- [ ] Contact form added
- [ ] Footer added
- [ ] All pages created
- [ ] Previewed and tested
- [ ] Published

---

**Site URLs:**
- Dashboard: https://manage.wix.com/dashboard/c13ae8c5-7053-4f2d-9a9a-371869be4395
- DEV Site: https://banf1.wixsite.com/banf (after publish)
- GitHub Repo: https://github.com/ranadhir19/banf1
