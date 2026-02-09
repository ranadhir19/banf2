# BANF Wix Deployment Guide - Kolkata Theme

## 🎨 Visual Theme: West Bengal / Kolkata

This guide covers deploying the new Kolkata-themed BANF website to Wix.

---

## 📁 Files to Deploy

### Wix Velo Page Code Files
| File | Target Page | Description |
|------|-------------|-------------|
| `LandingPage.velo.js` | Home | Main landing page with Kolkata theme |
| `EventsPage.velo.js` | Events | Events calendar and past events |
| `GalleryPage.velo.js` | Gallery | Photo/video gallery with filters |
| `AboutPage.velo.js` | About | Mission, EC members, history |

### HTML Reference Files (Design Specs)
| File | Description |
|------|-------------|
| `landing-page-kolkata.html` | Landing page design reference |
| `events-page.html` | Events page design reference |
| `gallery-page.html` | Gallery page design reference |
| `about-page.html` | About page design reference |

### Test Files
| File | Description |
|------|-------------|
| `comprehensive_api_test.js` | Full API test suite |

---

## 🎨 Kolkata Color Palette

Apply these colors in Wix Site Settings > Colors:

```
Primary (Saffron):     #FF6B35
Secondary (Burgundy):  #8B0000
Accent (Gold):         #D4AF37
Success (Bengal Green): #006A4E
Dark (Navy):           #1a1a2e
Background (Cream):    #FFF8E7
```

### CSS Variable Mapping
```css
--saffron: #FF6B35;
--saffron-dark: #E85A24;
--burgundy: #8B0000;
--bengal-green: #006A4E;
--gold: #D4AF37;
--navy: #1a1a2e;
```

---

## 📝 Deployment Steps

### Step 1: Update Site Colors
1. Go to Wix Editor > Site Design > Colors
2. Set Primary Color to `#FF6B35` (Saffron)
3. Set Secondary Color to `#8B0000` (Burgundy)
4. Set Accent Color to `#D4AF37` (Gold)
5. Save changes

### Step 2: Update Fonts
1. Go to Site Design > Fonts
2. Set Heading Font to "Playfair Display"
3. Set Body Font to "Inter"
4. Add "Hind Siliguri" for Bengali text support

### Step 3: Deploy Page Code

#### Landing Page (Home)
1. Open Home page in Wix Editor
2. Click "Dev Mode" > Turn on
3. Copy contents of `LandingPage.velo.js` to page code
4. Save

#### Events Page
1. Create new page named "Events"
2. Turn on Dev Mode
3. Copy `EventsPage.velo.js` to page code
4. Add these elements:
   - `#eventsRepeater` (Repeater for events)
   - `#timelineRepeater` (Repeater for timeline)
   - `#filterAll`, `#filterPuja`, `#filterCultural`, `#filterFestival` (Buttons)
   - `#headerStrip` (Strip for page header)
5. Save

#### Gallery Page
1. Create new page named "Gallery"
2. Turn on Dev Mode
3. Copy `GalleryPage.velo.js` to page code
4. Add these elements:
   - `#photoGallery` (Repeater/Gallery widget)
   - `#videoGallery` (Repeater for videos)
   - Filter buttons: `#filterAll`, `#filterDurga`, `#filterSaraswati`, `#filterBoishakh`, `#filterCultural`
5. Save

#### About Page
1. Create new page named "About"
2. Turn on Dev Mode
3. Copy `AboutPage.velo.js` to page code
4. Add these elements:
   - `#ecRepeater` (Repeater for EC members)
   - `#pastCommitteesRepeater` (Repeater/Accordion)
   - `#missionCard`, `#visionCard`, `#valuesCard` (Containers)
   - Stats: `#yearsCount`, `#membersCount`, `#eventsCount`
5. Save

### Step 4: Update CMS Collections

Ensure these collections exist with required fields:

#### Events Collection
```json
{
  "title": "string",
  "description": "string", 
  "eventDate": "date",
  "location": "string",
  "category": "string",
  "isFeatured": "boolean"
}
```

#### ExecutiveCommittee Collection
```json
{
  "name": "string",
  "position": "string",
  "year": "string",
  "avatarUrl": "string",
  "displayOrder": "number",
  "responsibility": "string"
}
```

#### Gallery Collection
```json
{
  "title": "string",
  "imageUrl": "string",
  "category": "string",
  "year": "number",
  "description": "string"
}
```

### Step 5: Add 2025-26 EC Members Data

Add these records to ExecutiveCommittee collection:

| name | position | year | displayOrder |
|------|----------|------|--------------|
| Dr Ranadhir Ghosh | President | 2025-26 | 1 |
| Partha Mukhopadhyay | Vice President | 2025-26 | 2 |
| Amit Chandak | Treasurer | 2025-26 | 3 |
| Dr Payel Banerjee | General Secretary | 2025-26 | 4 |
| Dr Moumita Ghosh | Cultural Secretary | 2025-26 | 5 |
| Banty Dutta | Food Coordinator | 2025-26 | 6 |
| Rajanya Ghosh | Event Planner | 2025-26 | 7 |
| Rwiti Choudhury | Puja Coordinator | 2025-26 | 8 |

### Step 6: Add 2025 Events Data

Add these records to Events collection:

| title | eventDate | category | isFeatured |
|-------|-----------|----------|------------|
| Saraswati Puja 2025 | 2025-02-15 | Puja | false |
| Basant Bahaar | 2025-03-20 | Cultural | false |
| Pohela Boishakh 1432 | 2025-04-14 | Festival | true |
| Anandadhara 2025 | 2025-06-15 | Cultural | true |
| Shrabono Sondha | 2025-08-10 | Cultural | false |
| Durga Puja 2025 | 2025-10-01 | Puja | true |

---

## 🧪 Testing

### Run API Tests

1. Open Wix Editor Dev Console
2. Import and run test suite:

```javascript
import { runComprehensiveApiTest } from 'backend/tests/comprehensive_api_test.js';

// In dev console
runComprehensiveApiTest().then(results => {
    console.log('Test Results:', results);
});
```

### Manual Testing Checklist

- [ ] Landing page loads with Kolkata colors
- [ ] Bengali text displays correctly (নর্থ ফ্লোরিডার বাঙালি সমিতি)
- [ ] Events display upcoming 2025 events
- [ ] Gallery filters work (All/Durga/Saraswati/etc.)
- [ ] EC members show with correct positions
- [ ] Membership tiers display ($50/$100/$250)
- [ ] Radio player connects to Bengali stations
- [ ] Mobile responsive design works
- [ ] Animation effects on scroll

---

## 🔧 Troubleshooting

### Issue: Colors not applying
- Check Site Design > Colors is updated
- Clear browser cache
- Republish site

### Issue: Bengali text not showing
- Ensure "Hind Siliguri" font is installed
- Check text encoding (UTF-8)

### Issue: Events not loading
- Verify Events collection has data
- Check collection permissions (public read)
- Review Velo console for errors

### Issue: EC members missing
- Add records to ExecutiveCommittee collection
- Verify year field matches "2025-26"

---

## 📊 Expected Results

After deployment, the site should display:

1. **Landing Page**
   - Hero with burgundy-saffron gradient
   - Stats: 17+ years, 200+ members, 100+ events
   - President's message with Bengali toggle
   - 4 upcoming events preview
   - 6 gallery highlights
   - 3 membership tiers

2. **Events Page**
   - 6 events for 2025
   - Category filters
   - Past events timeline

3. **Gallery Page**
   - Photo grid with filters
   - Video section with YouTube thumbnails
   - Lightbox functionality

4. **About Page**
   - Mission/Vision/Values cards
   - History timeline (2008-2025)
   - 8 EC members for 2025-26
   - Past committees accordion

---

## 📞 Support

For deployment assistance:
- Email: webmaster@banf-jacksonville.org
- BANF Technical Team

---

*Last Updated: January 2025*
*Theme: Kolkata/West Bengal Visual Design*
*EC: 2025-26 (Dr. Ranadhir Ghosh, President)*
