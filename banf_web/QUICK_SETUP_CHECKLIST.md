# BANF Wix Setup - Quick Checklist

## Login to Wix
- [ ] Go to: https://www.wix.com
- [ ] Login: Banfjax@gmail.com / Banfec2022
- [ ] Open your BANF site in the Editor

---

## Enable Velo Dev Mode
- [ ] In Editor → Click "Dev Mode" in top menu bar
- [ ] Click "Turn on Dev Mode"
- [ ] You should see a code panel appear at bottom

---

## Create CMS Collections (5 main ones)

### 1. Sponsors Collection
- [ ] Click "CMS" icon (left sidebar) → "Add Collection"
- [ ] Name: `Sponsors`
- [ ] Add these fields:
  - `name` (Text)
  - `level` (Text) - Gold/Silver/Bronze
  - `amount` (Number)
  - `contact` (Text)
  - `email` (Text)
  - `phone` (Text)
  - `logo` (Image)
  - `website` (URL)
  - `startDate` (Date)
  - `endDate` (Date)
  - `status` (Text) - Active/Pending/Expired

### 2. Documents Collection
- [ ] Add Collection → Name: `Documents`
- [ ] Fields:
  - `title` (Text)
  - `category` (Text)
  - `file` (Document/File)
  - `description` (Text)
  - `uploadDate` (Date)
  - `accessLevel` (Text) - Public/Members/Admin

### 3. Events Collection
- [ ] Add Collection → Name: `Events`
- [ ] Fields:
  - `title` (Text)
  - `date` (Date)
  - `time` (Text)
  - `location` (Text)
  - `description` (Rich Text)
  - `image` (Image)
  - `registrationLink` (URL)

### 4. BoardMembers Collection
- [ ] Add Collection → Name: `BoardMembers`
- [ ] Fields:
  - `name` (Text)
  - `title` (Text)
  - `email` (Text)
  - `bio` (Rich Text)
  - `photo` (Image)
  - `term` (Text)

### 5. NewsUpdates Collection
- [ ] Add Collection → Name: `NewsUpdates`
- [ ] Fields:
  - `title` (Text)
  - `content` (Rich Text)
  - `publishDate` (Date)
  - `image` (Image)
  - `category` (Text)

---

## Add Backend Code
- [ ] In Code Panel → Click "Backend" folder
- [ ] Right-click → "New .js file"
- [ ] Create these files (copy from `velo_backend` folder):

| File to Create | Copy From |
|----------------|-----------|
| `sponsors.jsw` | `velo_backend/sponsors.jsw` |
| `documents.jsw` | `velo_backend/documents.jsw` |
| `events.jsw` | `velo_backend/events.jsw` |
| `members.jsw` | `velo_backend/members.jsw` |
| `auth.jsw` | `velo_backend/auth.jsw` |

---

## Test It
- [ ] Click "Preview" to test your site
- [ ] Try adding a sponsor in CMS
- [ ] Verify it shows on site

---

## Publish
- [ ] Click "Publish" when ready
- [ ] Your site is live!

---

## Files Ready to Copy

All your Velo backend code is in:
```
C:\projects\survey\banf_web\velo_backend\
```

All page code is in:
```
C:\projects\survey\banf_web\wix_pages\
```

Just open each file, copy the content, and paste into Wix Editor!
