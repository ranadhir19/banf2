# 🚀 QUICK SETUP GUIDE - BANF Homepage in 5 Minutes

Since Wix doesn't auto-deploy page structure from GitHub, here's the **fastest way** to get the new homepage working:

---

## Option 1: HTML Embed (FASTEST - 2 minutes)

### Step 1: Open Wix Editor
1. Go to https://manage.wix.com
2. Login with `Banfjax@gmail.com`
3. Find your **banf1** (DEV) site
4. Click **Edit Site**

### Step 2: Enable Dev Mode
1. Look for **Dev Mode** toggle in top-left
2. Turn it **ON**

### Step 3: Add Full-Page HTML Embed
1. Click **+** (Add Elements)
2. Go to **Embed & Social** → **Embed Code** → **Popular Embeds** → **Custom Embed**
3. Drag it to your page
4. Resize to **full page width and height**
5. Click the embed → **Set Address**
6. Switch to **Code** tab
7. Paste the HTML from `landing_embed.html` (see below)

### Step 4: Publish
1. Click **Publish** (top right)
2. Done! ✅

---

## Option 2: Use Wix Built-in Components (Better for SEO)

### Required Elements to Add Manually:

#### Hero Section
| Element Type | Wix ID | Content |
|-------------|--------|---------|
| Text | `#txtBengaliWelcome` | স্বাগতম |
| Text | `#txtEnglishWelcome` | Welcome to BANF |
| Text | `#txtTagline` | Preserving Bengali culture... |
| Button | `#btnJoinBANF` | Join Our Community |
| Button | `#btnExploreEvents` | Explore Events |

#### Stats Strip
| Element Type | Wix ID | Content |
|-------------|--------|---------|
| Text | `#txtMemberCount` | 500+ |
| Text | `#txtMemberLabel` | Active Members |
| Text | `#txtEventCount` | 50+ |
| Text | `#txtEventLabel` | Events Yearly |
| Text | `#txtYearsCount` | 35+ |
| Text | `#txtYearsLabel` | Years Strong |

#### Quick Access Icons (Repeater or Boxes)
| Element | Wix ID | Link |
|---------|--------|------|
| Box | `#quickEvents` | /events |
| Box | `#quickMembers` | /members |
| Box | `#quickRadio` | /radio |
| Box | `#quickMagazine` | /magazine |
| Box | `#quickGallery` | /gallery |
| Box | `#quickVolunteer` | /volunteer |

#### Events Section
| Element Type | Wix ID |
|-------------|--------|
| Repeater | `#repeaterEvents` |

#### Radio Section
| Element Type | Wix ID | Content |
|-------------|--------|---------|
| Text | `#txtRadioStatus` | 🔴 LIVE |
| Text | `#txtNowPlaying` | Bengali Music Hour |
| Button | `#btnPlayRadio` | ▶ Play |

#### Contact Form
| Element Type | Wix ID |
|-------------|--------|
| Input | `#inputContactName` |
| Input | `#inputContactEmail` |
| Input | `#inputContactSubject` |
| TextBox | `#inputContactMessage` |
| Button | `#btnSubmitQuickContact` |

---

## How to Set Element IDs in Wix Editor

1. **Select the element** you want to set ID for
2. **Right-click** → **View Properties** 
   OR click the **⚙️ (Settings)** icon
3. In the Properties panel, find **ID** field
4. Type the ID (without the #)
5. Press Enter

Example: For `#txtBengaliWelcome`:
- Select the text element
- Set ID to: `txtBengaliWelcome`

---

## GitHub Pull (For Code Sync)

If your code isn't updating:

1. In Wix Editor, open **Code Panel** (left sidebar, `{ }` icon)
2. At bottom, find **Source Control** or **GitHub** icon
3. Click **Pull** to get latest code from GitHub
4. You should see `Home.js` updated with all integrations

---

## Testing After Setup

Once elements are added with correct IDs:

1. **Preview** the site
2. Check console for errors (F12 → Console)
3. Verify:
   - ✅ Stats load (member count, event count)
   - ✅ Events repeater populates
   - ✅ Radio status shows
   - ✅ Contact form submits
   - ✅ Quick access buttons navigate correctly

---

## Troubleshooting

### "Element not found" errors
- Double-check the ID matches exactly (case-sensitive)
- Make sure you removed the `#` when setting ID in Wix

### Code not running
- Ensure Dev Mode is ON
- Check that `Home.js` exists in Code Panel under Pages → Home

### Styles not applying
- The `Home.js` file includes dynamic styling
- For full styling, use the HTML embed approach

---

## Files Reference

| File | Purpose |
|------|---------|
| `wix-github-repo/src/pages/Home.js` | All homepage logic + backend integrations |
| `wix-github-repo/src/pages/Home.html` | Design reference (not used by Wix directly) |
| `landing_embed.html` | Ready-to-paste full HTML for embed |

---

**Need help?** The browser automation script is at `wix_auto_setup.py` - run it to auto-login and assist with setup.
