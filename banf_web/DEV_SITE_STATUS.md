# BANF Wix Dev Site Status Report
**Generated:** 2026-02-08

## ✅ WORKING

### API Key
```
IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjE1MWNjZDg0LTQ2OTYtNDQwOS1hNmRkLWM2Y2FiZGJlZDljYlwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcIjliYzc1ZTljLWNkNTYtNDUxYy1hNDU2LTg2NzQ1ZmViY2RhNFwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCJjNjJmOTQzYy0yYWZiLTQ2YjctYTM4MS1mYTczNTJmY2NmYjJcIn19IiwiaWF0IjoxNzcwNTc5MzQ0fQ.g3EY1YVaCgmhDFxDPXv_18xrhRx1-dKhTc3EwMPIeG-qnOVpuOAnvli9TiV94rDunkgj7Mjcb96_RfijUkHU12L9MXzqdyLicoYZD6g7L1KZp97QllmMIAkm7vnWucVBK7J2B2nj1JR5m1dYwRx_zZbCiGQRSs-d95rFNeyleo0wW8tH448SczxrOqOoOxuuwRoUWBxMpaWtYT2cGJFhUNPalmDy097_TMC3mHtRejLmzBXd0RHglaIjDrZI4OZSDDQsGs2RPktLwCytD8murY-ffjHbo9U4hUFQOeL3ysTm_YpyAKWMG-sMK0o5Y9E_L-XZf7xGV6e5_0VhKpe_QA
```

### Sites
| Site | ID | URL | Status |
|------|----|-----|--------|
| **Dev (Banf1)** | `c13ae8c5-7053-4f2d-9a9a-371869be4395` | https://banfwix.wixsite.com/banf1 | ✅ 200 OK |
| **Production** | `6a4f0362-0394-4e28-8559-f6145dd414e0` | https://www.jaxbengali.org | ✅ 200 OK |

### Account Info
- **Account ID:** `c62f943c-2afb-46b7-a381-fa7352fccfb2`
- **Total sites:** 7

---

## 🔴 PROBLEM: Dev Site Has No Collections

| Site | Total Collections | Custom Collections |
|------|------------------|-------------------|
| Production | 134 | 130 |
| **Dev (Banf1)** | **4** | **0** ❌ |

The dev site only has the default system collections (Members/Badges, Members/FullData, etc.)

---

## 📋 TO DO: Fix Dev Site for Testing

### Option 1: Create Collections via API (Recommended)
Run the collection creation script against the dev site:
```bash
python create_collections_on_dev.py
```

This will create all 134 collections matching production.

### Option 2: Copy from Production in Wix Dashboard
1. Go to https://manage.wix.com/dashboard/c13ae8c5-7053-4f2d-9a9a-371869be4395/content-manager
2. Manually create collections matching production

### Option 3: Transfer/Clone Site
Use Wix's site transfer feature to clone production to dev.

---

## 🧪 Testing After Collections Created

1. **Test Collection Access:**
   ```python
   # GET https://www.wixapis.com/wix-data/v2/collections
   # Header: wix-site-id: c13ae8c5-7053-4f2d-9a9a-371869be4395
   ```

2. **Test Data Operations:**
   - Create test items
   - Query items
   - Update items
   - Delete items

3. **Test Backend Functions:**
   - Access dev site: https://banfwix.wixsite.com/banf1
   - Test page functionality with Velo code

---

## GitHub Sync Status
- **Home.mainPage.js** ✅ Pushed to GitHub
- **Backend modules** Need to verify sync
