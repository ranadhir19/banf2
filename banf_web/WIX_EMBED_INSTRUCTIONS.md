# 🚀 BANF Landing Page - Wix Embed Instructions

## Option 1: HTML iframe (Recommended - Easiest)

### Step 1: Host the HTML File
First, you need to host the landing page HTML somewhere accessible. Options:

**A) GitHub Pages (Free)**
1. Go to your GitHub repo settings
2. Enable GitHub Pages
3. Upload `wix-embed-landing.html`
4. Your URL will be: `https://[username].github.io/[repo]/wix-embed-landing.html`

**B) Wix Static Hosting**
1. Upload to Wix Media Manager
2. Get the public URL

**C) Use Current Wix Static URL** (if already uploaded)
```
https://static.wixstatic.com/shapes/c62f94_[file-id].html
```

### Step 2: Add HTML iframe in Wix Editor

1. **Open Wix Editor** → Click `+` (Add Elements)
2. Navigate to **Embed Code** → **Embed HTML**
3. Drag to your page
4. Click **Enter Code**
5. Paste this code:

```html
<iframe 
    src="YOUR_HOSTED_URL_HERE" 
    style="width:100%; height:100vh; border:none;"
    scrolling="auto"
    frameborder="0"
></iframe>
```

6. Set iframe dimensions:
   - Width: 100%
   - Height: 100% (or specific like 5000px)

---

## Option 2: Full-Page Custom Element

### Step 1: Create Custom Element in Wix

1. In Wix Editor with **Dev Mode ON**
2. Click **{} Custom Elements** in the left panel
3. Click **+ Create New**
4. Name it: `banf-landing-page`

### Step 2: Add Custom Element Code

Paste this in the Custom Element editor:

```javascript
// BANF Landing Page Custom Element
const html = `
<!DOCTYPE html>
<html>
<head>
    <style>/* All CSS from wix-embed-landing.html */</style>
</head>
<body>
    <!-- All HTML content -->
</body>
</html>
`;

class BanfLanding extends HTMLElement {
    connectedCallback() {
        const shadow = this.attachShadow({mode: 'open'});
        const iframe = document.createElement('iframe');
        iframe.srcdoc = html;
        iframe.style.cssText = 'width:100%;height:100%;border:none;';
        shadow.appendChild(iframe);
    }
}
customElements.define('banf-landing', BanfLanding);
```

---

## Option 3: Wix Blocks (Advanced)

### Create a Wix Block Component

1. Open **Wix Blocks** from the left sidebar
2. Create a new Widget
3. Add an **HTML iFrame** element
4. Configure to load your hosted HTML

---

## 📋 Quick Setup Checklist

### In Wix Editor:
- [ ] Open site in Wix Editor
- [ ] Enable Dev Mode (if not already)
- [ ] Navigate to Home page
- [ ] Add → Embed Code → Embed HTML
- [ ] Paste iframe code with hosted URL
- [ ] Resize to full width/height
- [ ] Preview and test
- [ ] Publish site

---

## 🎨 What's Included in the Embed

| Section | Description |
|---------|-------------|
| **Hero** | Bengali welcome, gradient background, CTA buttons |
| **Stats** | 80+ families, 10+ events, 17 years, 45+ sponsors |
| **President's Message** | Dr. Ranadhir Ghosh with Bengali/English toggle |
| **EC Team** | 8 executive committee members with cards |
| **Events** | 2026 calendar - Durga Puja, Saraswati, Spandan |
| **Radio** | BANF Radio player section |
| **Membership** | Individual ($50), Family ($100), Senior ($35) |
| **Contact** | Contact form |
| **Footer** | Social links, quick links, contact info |

---

## 🔧 Customization

### Change Colors (in CSS variables):
```css
:root {
    --banf-orange: #ff6b35;     /* Primary orange */
    --banf-deep-red: #8B0000;   /* Deep red */
    --banf-green: #006A4E;      /* Bangladesh green */
    --gold: #D4AF37;            /* Gold accent */
}
```

### Update Content:
- EC members in the EC Team section
- Events in the Events section
- Pricing in Membership section
- Contact info in Footer

---

## ⚡ Quick Deploy Commands

### Upload to Wix via GitHub sync:
```bash
cd C:\projects\survey\banf_web\wix-github-repo
cp ../wix-embed-landing.html src/public/
git add .
git commit -m "Add embeddable landing page"
git push
```

Then in Wix: **Pull from GitHub** → File will appear in public folder

---

## 📱 Mobile Responsive

The embedded page is fully responsive:
- Desktop: Full layout
- Tablet: Adjusted grid
- Mobile: Stacked layout, smaller fonts

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| iframe doesn't load | Check URL is correct and publicly accessible |
| Content cut off | Increase iframe height |
| Fonts not loading | Ensure fonts.googleapis.com is allowed |
| Bootstrap not loading | Check cdn.jsdelivr.net is allowed |
| Scrolling issues | Add `scrolling="auto"` to iframe |

---

## 🎯 Next Steps

1. **Upload HTML** to GitHub Pages or Wix static
2. **Get public URL**
3. **Add iframe** in Wix Editor
4. **Test** on desktop and mobile
5. **Publish** the site

The landing page will display exactly as designed with all sections working!
