# BANF Premium Landing Page - Wix Editor Setup Guide

## 🎨 Design Overview

This guide helps you recreate the stunning premium landing page in Wix Editor. The design features:
- **Bangladesh flag colors**: Green (#006A4E) and Red (#F42A41) with Gold accents (#FFD700)
- **Low cognitive load**: Clear visual hierarchy, grouped features
- **Mobile responsive**: Adapts beautifully to all screen sizes

---

## 📐 Page Structure

```
┌─────────────────────────────────────────────────────────────┐
│  🔝 NAVBAR (Fixed, Transparent → White on scroll)           │
├─────────────────────────────────────────────────────────────┤
│  🦸 HERO SECTION (Full viewport height, Green gradient)     │
│  • Stats: 500+ Members, 35+ Years, 50+ Events               │
│  • CTA: "Become a Member" + "Upcoming Events"               │
├─────────────────────────────────────────────────────────────┤
│  ⚡ QUICK ACCESS BAR (Floating cards, White)                │
│  • Pay Membership | Events | Radio | Magazine | Guide       │
├─────────────────────────────────────────────────────────────┤
│  ✨ FEATURES SECTION (Light gray background)                │
│  • 6 feature cards in 3-column grid                         │
├─────────────────────────────────────────────────────────────┤
│  📅 EVENTS SECTION (White background)                       │
│  • Featured event (large) + Upcoming list (sidebar)         │
├─────────────────────────────────────────────────────────────┤
│  💳 MEMBERSHIP CTA (Green gradient)                         │
│  • Benefits list + Pricing cards                            │
├─────────────────────────────────────────────────────────────┤
│  🗺️ COMMUNITY RESOURCES (White)                             │
│  • 4 resource cards: Restaurants, Grocery, Doctors, Services│
├─────────────────────────────────────────────────────────────┤
│  📻 RADIO SECTION (Dark gradient)                           │
│  • Mini player preview + Features list                      │
├─────────────────────────────────────────────────────────────┤
│  💬 TESTIMONIALS (Light gray)                               │
│  • 3 testimonial cards                                      │
├─────────────────────────────────────────────────────────────┤
│  🔻 FOOTER (Dark gradient)                                  │
│  • Logo, Links (5 columns), Social, Copyright               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Color Palette

Add these to your Wix site colors:

| Name | Hex Code | Usage |
|------|----------|-------|
| Green Primary | `#006A4E` | Main brand color, buttons |
| Green Light | `#00A86B` | Gradients, accents |
| Green Dark | `#004D3D` | Headers, footer |
| Red Accent | `#F42A41` | Badges, highlights |
| Gold | `#FFD700` | CTAs, featured items |
| Gold Light | `#FFF4CC` | Badges background |
| Off White | `#F8F9FA` | Section backgrounds |
| Gray 500 | `#6C757D` | Body text |
| Gray 900 | `#212529` | Headings |

---

## 🔝 Section 1: NAVBAR

### Wix Editor Elements

1. **Container Box** (ID: `sectionNavbar`)
   - Full width, height: 70px
   - Background: Transparent (changes on scroll via code)
   - Position: Fixed to top
   - Z-Index: 100

2. **Logo** 
   - **Icon Box** (ID: `boxLogoIcon`): 50x50px, Green gradient, rounded 12px
   - **Text** (ID: `txtLogo`): "BANF", Playfair Display, 24px, White

3. **Navigation Links** (ID: `boxNavLinks`)
   - Horizontal layout, gap: 8px
   - Items: Home, About, Events, Gallery, Radio, Magazine, Guide
   - Style: Poppins 15px, White, padding 10px 18px

4. **Buttons**
   - **Login Button** (ID: `btnLogin`): Outline style, White border
   - **Join Button** (ID: `btnJoin`): Gold gradient, Dark text

### Code Connection
```javascript
// Elements to connect:
#sectionNavbar, #boxLogoIcon, #txtLogo, #boxNavLinks
#btnLogin, #btnJoin, #btnLogout (hidden by default)
#btnMobileMenu (show on mobile only)
#boxMobileNav (hidden by default)
```

---

## 🦸 Section 2: HERO

### Wix Editor Elements

1. **Section Strip** (ID: `sectionHero`)
   - Full viewport height (100vh)
   - Background: Green gradient (`#006A4E` → `#004D3D`)
   - Add subtle pattern overlay

2. **Two-Column Layout**
   - Left: Content (60%)
   - Right: Visual (40%)

3. **Left Content** (ID: `boxHeroContent`)
   - **Badge** (ID: `boxHeroBadge`): "⭐ Serving Jacksonville Since 1990"
   - **Title** (ID: `txtHeroTitle`): "Celebrating Bengali Heritage in North Florida"
   - **Subtitle** (ID: `txtHeroSubtitle`): Description text
   
4. **Statistics Row**
   - **Stat 1** (ID: `txtStatMembers`): "500+"  / "Member Families"
   - **Stat 2** (ID: `txtStatYears`): "35+" / "Years Strong"
   - **Stat 3** (ID: `txtStatEvents`): "50+" / "Events/Year"

5. **CTA Buttons**
   - **Primary** (ID: `btnHeroJoin`): "Become a Member" - Gold
   - **Secondary** (ID: `btnHeroEvents`): "Upcoming Events" - Outline

6. **Right Visual** (ID: `boxHeroVisual`)
   - Large image with rounded corners
   - Floating cards:
     - Top-right: "Next Event: Saraswati Puja"
     - Bottom-left: "BANF Radio: Live 24/7"

### Typography
- Title: Playfair Display, 56px, Bold, White
- Subtitle: Poppins, 20px, Light, White/90%
- Stats Numbers: Playfair Display, 40px, Bold, Gold
- Stats Labels: Poppins, 14px, White/80%

---

## ⚡ Section 3: QUICK ACCESS BAR

### Wix Editor Elements

1. **Container** (ID: `sectionQuickAccess`)
   - Margin top: -60px (overlaps hero)
   - Max width: 1200px, centered
   - Z-Index: 10

2. **Grid of 5 Cards**
   - Background: White
   - Border radius: 20px
   - Box shadow: Large

3. **Each Quick Item** (use Repeater or individual boxes)
   - ID pattern: `btnQuick[Feature]`
   - Icon (60x60, green background)
   - Title (Poppins 15px, Bold)
   - Subtitle (Poppins 13px, Gray)

| Button ID | Icon | Title | Link |
|-----------|------|-------|------|
| `btnQuickMembership` | 💳 | Pay Membership | /member-payment |
| `btnQuickEvents` | 📅 | Events Calendar | /events |
| `btnQuickRadio` | 🎧 | BANF Radio | /radio |
| `btnQuickMagazine` | 📖 | E-Magazine | /magazine |
| `btnQuickGuide` | 🗺️ | Jacksonville Guide | /guide |

---

## ✨ Section 4: FEATURES

### Wix Editor Elements

1. **Section** (ID: `sectionFeatures`)
   - Background: #F8F9FA (off-white)
   - Padding: 100px vertical

2. **Section Header**
   - Badge: "✨ What We Offer"
   - Title: "Everything for Our Bengali Community"
   - Subtitle: Description

3. **Repeater** (ID: `repeaterFeatures`) - 3 columns, 2 rows

4. **Feature Card Template**
   - ID: `boxFeatureCard`
   - Background: White
   - Border radius: 20px
   - Padding: 35px
   - Hover: Lift + shadow + green border

| Icon | Title | Description |
|------|-------|-------------|
| 🕉️ | Cultural Events | Durga Puja, Saraswati Puja, Pohela Boishakh... |
| 📻 | 24/7 Radio Station | Bengali music, news, and programs... |
| 📰 | E-Magazine | Quarterly digital magazine... |
| 🏪 | Jacksonville Guide | Find Bengali restaurants, grocery stores... |
| 📊 | Community Surveys | Have your voice heard... |
| 📄 | Meeting Minutes | Stay informed with EC meeting minutes... |

---

## 📅 Section 5: EVENTS

### Wix Editor Elements

1. **Two-Column Layout**
   - Left (65%): Featured event
   - Right (35%): Upcoming list

2. **Featured Event Card** (ID: `boxFeaturedEvent`)
   - Full-height image
   - Gradient overlay (transparent → black)
   - Content at bottom:
     - Badge (ID: `badgeFeatured`): "🔥 Featured Event"
     - Title (ID: `txtFeaturedTitle`)
     - Description (ID: `txtFeaturedDesc`)
     - Button (ID: `btnFeaturedRegister`): "Register Now"

3. **Events Repeater** (ID: `repeaterEvents`)
   - 4 items max
   - Each item (ID: `boxEventCard`):
     - Date box: Day (large) + Month (small)
     - Title + Venue

---

## 💳 Section 6: MEMBERSHIP CTA

### Wix Editor Elements

1. **Section** (ID: `sectionMembership`)
   - Background: Green gradient
   - Decorative circle overlay

2. **Two-Column Layout**
   - Left: Benefits content
   - Right: Pricing cards

3. **Benefits List** (ID: `boxMembershipBenefits`)
   - 6 items in 2x3 grid:
     - 🎫 Event Discounts
     - 🗳️ Voting Rights
     - 👥 Community Access
     - 👶 Youth Programs
     - 📖 E-Magazine
     - 🎧 Radio Requests

4. **Pricing Repeater** (ID: `repeaterMembership`)
   - 4 cards stacked vertically
   - Featured card: Gold border, scale 1.02

---

## 🗺️ Section 7: COMMUNITY RESOURCES

### Wix Editor Elements

1. **4-Column Grid** (ID: `repeaterResources`)

2. **Resource Card Template**
   - Image (height: 160px, hover zoom)
   - Title
   - Description
   - "Explore →" link

---

## 📻 Section 8: RADIO

### Wix Editor Elements

1. **Section** (ID: `sectionRadio`)
   - Background: Dark gradient (#1a1a2e → #16213e)

2. **Two-Column Layout**
   - Left: Content + features
   - Right: Mini player

3. **Radio Player** (ID: `boxRadioPlayer`)
   - Album art circle (animated pulse)
   - Now Playing text
   - Play/Pause button (ID: `btnRadioPlay`)
   - Hidden audio element (ID: `audioRadio`)

---

## 💬 Section 9: TESTIMONIALS

### Wix Editor Elements

1. **3-Column Grid** (ID: `repeaterTestimonials`)

2. **Testimonial Card**
   - Star rating
   - Quote text (italic)
   - Author info:
     - Avatar (initials in circle)
     - Name
     - Member since

---

## 🔻 Section 10: FOOTER

### Wix Editor Elements

1. **Section** (ID: `sectionFooter`)
   - Background: Dark gradient
   - Padding: 80px top, 30px bottom

2. **5-Column Grid**
   - Col 1 (wider): Brand info + social
   - Col 2-5: Link lists

3. **Footer Links** (use Text with link)
   - Quick Links: About, Events, Gallery, Membership, Contact
   - Resources: Radio, Magazine, Guide, Minutes, Surveys
   - Members: Login, Pay Dues, Feedback, Sponsors
   - Contact: Email, Location, Phone

4. **Social Icons** (ID: `boxSocialLinks`)
   - Facebook, Instagram, YouTube, WhatsApp

5. **Bottom Bar**
   - Copyright text
   - Privacy | Terms | Admin links

---

## 📱 Mobile Responsiveness

### Breakpoints to Configure

1. **Desktop** (> 1200px): Full layout
2. **Tablet** (768px - 1200px):
   - 2-column grids → 1 column
   - Hide hero visual
   - Stack membership content
3. **Mobile** (< 768px):
   - Hide nav links, show hamburger menu
   - Stack everything vertically
   - Quick access: 2 columns then 1
   - Reduce padding/margins by 50%

---

## 🔗 Code Connection Checklist

Copy `LandingPage.velo.js` to your page code and ensure these element IDs match:

### Navbar
- [ ] `#sectionNavbar`
- [ ] `#txtLogo`
- [ ] `#btnLogin`
- [ ] `#btnJoin`
- [ ] `#btnLogout`
- [ ] `#btnMobileMenu`
- [ ] `#boxMobileNav`

### Hero
- [ ] `#boxHeroContent`
- [ ] `#txtStatMembers`
- [ ] `#txtStatYears`
- [ ] `#txtStatEvents`
- [ ] `#btnHeroJoin`
- [ ] `#btnHeroEvents`

### Quick Access
- [ ] `#sectionQuickAccess`
- [ ] `#btnQuickMembership`
- [ ] `#btnQuickEvents`
- [ ] `#btnQuickRadio`
- [ ] `#btnQuickMagazine`
- [ ] `#btnQuickGuide`

### Features
- [ ] `#sectionFeatures`
- [ ] `#repeaterFeatures`

### Events
- [ ] `#sectionEvents`
- [ ] `#boxFeaturedEvent`
- [ ] `#txtFeaturedTitle`
- [ ] `#txtFeaturedDesc`
- [ ] `#imgFeatured`
- [ ] `#btnFeaturedRegister`
- [ ] `#repeaterEvents`

### Membership
- [ ] `#sectionMembership`
- [ ] `#repeaterMembership`
- [ ] `#btnJoinNow`

### Resources
- [ ] `#sectionResources`
- [ ] `#repeaterResources`

### Radio
- [ ] `#sectionRadio`
- [ ] `#boxRadioPlayer`
- [ ] `#txtNowPlaying`
- [ ] `#btnRadioPlay`
- [ ] `#iconRadioPlay`
- [ ] `#audioRadio`

### Testimonials
- [ ] `#sectionTestimonials`
- [ ] `#repeaterTestimonials`

### Footer
- [ ] `#sectionFooter`
- [ ] All footer link buttons

---

## 🚀 Quick Implementation Steps

1. **Create New Page** named "Home" in Wix Editor
2. **Add Sections** one by one following this guide
3. **Set Element IDs** matching the code
4. **Copy Velo Code** from `LandingPage.velo.js`
5. **Connect CMS Collections**:
   - Events
   - Members
   - Testimonials
6. **Preview & Test** on all device sizes
7. **Publish!**

---

## 📸 Image Recommendations

Use high-quality images from Unsplash or your own:

| Section | Recommended Image |
|---------|------------------|
| Hero | Community gathering/celebration |
| Featured Event | Durga Puja or cultural celebration |
| Resources | Category-appropriate images |
| Radio | Music/audio visual |

---

## ✅ Final Checklist

- [ ] All colors match brand palette
- [ ] Typography is consistent (Playfair Display + Poppins)
- [ ] All links navigate correctly
- [ ] Mobile menu works
- [ ] Stats animate on load
- [ ] Events load from CMS
- [ ] Login/logout states work
- [ ] Radio player functional
- [ ] Footer links work
- [ ] Page loads under 3 seconds

---

**Need Help?** Refer to:
- `wix_pages/landing-page-premium.html` - Full HTML/CSS reference
- `velo_pages/LandingPage.velo.js` - Complete Velo code
