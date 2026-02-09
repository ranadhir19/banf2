# BANF Production Deployment Guide
## Complete Step-by-Step Instructions

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:
- [ ] All 158 collections are created (verified ✅)
- [ ] All Velo .jsw files are ready in `velo_backend/` (verified ✅)
- [ ] Production readiness test passes 98.9%+ (verified ✅)
- [ ] Wix account credentials available

---

## Step 1: Deploy Velo Backend Files

### Option A: Automated Deployment (Recommended)
```bash
cd C:\projects\survey\banf_web
python deploy_to_production.py
```

### Option B: Manual Deployment via Wix Editor

1. **Open Wix Editor**
   - Go to: https://manage.wix.com
   - Select your site → "Edit Site"

2. **Enable Dev Mode**
   - Click the **Dev Mode** toggle (top bar)
   - Or press `Ctrl+Shift+D`

3. **Create Backend Files**
   - In the left panel, expand **"backend"** folder
   - Right-click → **Add** → **Web Module (.jsw)**
   - For each file in `velo_backend/`:
     - Create new module with same name (without .jsw)
     - Copy-paste the file content
     - Press `Ctrl+S` to save

4. **Verify All 41 Modules**
   ```
   Required modules:
   - members.jsw, events.jsw, finance.jsw
   - surveys.jsw, complaints.jsw, radio.jsw
   - magazine.jsw, guide.jsw, admin.jsw
   - email.jsw, analytics-service.jsw, sponsor-management.jsw
   ... (see full list in velo_backend/)
   ```

---

## Step 2: Configure Custom Domain

### In Wix Dashboard:

1. Go to **Settings** → **Custom Domains**
2. Click **"Connect a Domain You Already Own"**
3. Enter: `jaxbengali.org`
4. Follow Wix instructions to update DNS

### DNS Configuration (at your registrar):

Add these DNS records:

| Type | Host | Value |
|------|------|-------|
| CNAME | www | `www.<siteid>.wixsite.com` |
| A | @ | `185.230.63.107` |
| A | @ | `185.230.63.186` |

Or use Wix nameservers:
- `ns1.wixdns.net`
- `ns2.wixdns.net`

### SSL Certificate:
- Wix automatically provisions SSL after DNS propagation
- Takes 24-48 hours to fully activate

---

## Step 3: Publish to Production

### Via Editor:
1. Click **"Publish"** button (top-right)
2. Review publish settings
3. Click **"Publish Now"**

### Verify Publication:
- Visit: https://banfwix.wixsite.com/banf1
- Check all pages load correctly
- Test key features (member registration, event listing)

---

## Step 4: Post-Deployment Verification

### Run Automated Tests:
```bash
cd C:\projects\survey\banf_web
python production_readiness_test.py
```

### Manual Verification Checklist:
- [ ] Homepage loads correctly
- [ ] Navigation works
- [ ] Events page shows events
- [ ] Membership registration works
- [ ] Donation form functions
- [ ] Contact form submits
- [ ] Admin area accessible
- [ ] Mobile responsive

---

## Step 5: Production Monitoring

### Set Up Monitoring:
1. **Wix Analytics** - Built-in traffic monitoring
2. **Error Logging** - Check AdminLogs collection
3. **Uptime Monitoring** - Use external service (UptimeRobot, etc.)

### Key Metrics to Watch:
- Page load times
- Form submission success rates
- API error rates (check EmailLogs, AdminLogs)
- User registration trends

---

## 🚨 Troubleshooting

### Common Issues:

**1. Velo Code Not Working**
- Ensure Dev Mode is enabled
- Check for syntax errors in .jsw files
- Verify collection names match exactly

**2. Domain Not Connecting**
- DNS propagation takes up to 48 hours
- Verify DNS records are correct
- Check for typos in domain name

**3. SSL Certificate Issues**
- Wait 24-48 hours after DNS setup
- Contact Wix support if persists

**4. Collections Not Found**
- Run: `python create_missing_collections.py`
- Verify collection names in Wix CMS

---

## 📞 Support Contacts

- **Wix Support**: https://support.wix.com
- **Domain Registrar**: Check your registrar's support
- **BANF Technical**: [Your contact info]

---

## 📁 File Locations

| Item | Location |
|------|----------|
| Velo Backend Files | `C:\projects\survey\banf_web\velo_backend\` |
| Test Scripts | `C:\projects\survey\banf_web\production_readiness_test.py` |
| Deployment Script | `C:\projects\survey\banf_web\deploy_to_production.py` |
| Screenshots | `C:\projects\survey\banf_web\screenshots\` |
| Deployment Report | `C:\projects\survey\banf_web\PRODUCTION_READINESS_REPORT.md` |

---

## ✅ Deployment Complete

After completing all steps:

1. Site is live at: https://www.jaxbengali.org
2. All Velo modules deployed
3. Custom domain configured
4. SSL active
5. Monitoring in place

**Congratulations! BANF is now in production! 🎉**
