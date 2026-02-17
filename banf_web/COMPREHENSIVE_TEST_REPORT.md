# BANF Website Comprehensive Test Report

**Generated:** 2026-02-17 14:55:09
**Test Suite:** comprehensive_test.py
**Target:** wix-embed-landing-v2.html + banf_archive.db

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Total Tests** | 179 |
| **Passed** | ✅ 179 |
| **Failed** | ❌ 0 |
| **Warnings** | ⚠️ 0 |
| **Pass Rate** | **100.0%** |

---

## ✅ HTML Structure (18/18 — 100%)

| Test | Status | Detail |
|------|--------|--------|
| HTML file exists | ✅ PASS |  |
| File size reasonable (677,049 chars) | ✅ PASS |  |
| Line count (12,715 lines) | ✅ PASS |  |
| Has <!DOCTYPE html> | ✅ PASS |  |
| Has <html> tag | ✅ PASS |  |
| Has <head> tag | ✅ PASS |  |
| Has <body> tag | ✅ PASS |  |
| Has closing </html> | ✅ PASS |  |
| Has viewport meta | ✅ PASS |  |
| Viewport allows zoom | ✅ PASS | Mobile accessibility |
| Has charset meta | ✅ PASS |  |
| Bootstrap CSS loaded | ✅ PASS |  |
| FontAwesome loaded | ✅ PASS |  |
| Has touch-action CSS | ✅ PASS |  |
| Has -webkit-overflow-scrolling | ✅ PASS |  |
| Has overscroll-behavior | ✅ PASS |  |
| No ondragstart on body | ✅ PASS |  |
| No onselectstart on body | ✅ PASS |  |

## ✅ Navigation (17/17 — 100%)

| Test | Status | Detail |
|------|--------|--------|
| Section: Hero/Header | ✅ PASS |  |
| Section: About | ✅ PASS |  |
| Section: Events | ✅ PASS |  |
| Section: Radio | ✅ PASS |  |
| Section: Membership | ✅ PASS |  |
| Section: Gallery/Photos | ✅ PASS |  |
| Section: Guide (Jacksonville) | ✅ PASS |  |
| Section: Contact/Footer | ✅ PASS |  |
| Has navigation bar | ✅ PASS |  |
| Has mobile nav toggle | ✅ PASS |  |
| Member Portal exists | ✅ PASS |  |
| Admin Dashboard exists | ✅ PASS |  |
| Portal: Portal Dashboard | ✅ PASS |  |
| Portal: Portal Events | ✅ PASS |  |
| Portal: Portal Radio | ✅ PASS |  |
| Portal: Portal Family | ✅ PASS |  |
| Portal: Portal Membership | ✅ PASS |  |

## ✅ Radio Player (44/44 — 100%)

| Test | Status | Detail |
|------|--------|--------|
| Play button exists | ✅ PASS |  |
| Skip forward button exists | ✅ PASS |  |
| Skip backward button exists | ✅ PASS |  |
| Now Playing element | ✅ PASS |  |
| Now Playing subtitle | ✅ PASS |  |
| Equalizer animation | ✅ PASS |  |
| Vinyl disc animation | ✅ PASS |  |
| Daily schedule defined | ✅ PASS |  |
| getCurrentScheduleSlot function | ✅ PASS |  |
| buildScheduleStrip function | ✅ PASS |  |
| playScheduleSlot function | ✅ PASS |  |
| Schedule strip visible (not hidden) | ✅ PASS |  |
| Schedule slot hour: 6 | ✅ PASS |  |
| Schedule slot hour: 8 | ✅ PASS |  |
| Schedule slot hour: 10 | ✅ PASS |  |
| Schedule slot hour: 12 | ✅ PASS |  |
| Schedule slot hour: 14 | ✅ PASS |  |
| Schedule slot hour: 16 | ✅ PASS |  |
| Schedule slot hour: 18 | ✅ PASS |  |
| Schedule slot hour: 20 | ✅ PASS |  |
| Schedule slot hour: 22 | ✅ PASS |  |
| Source tabs exist | ✅ PASS |  |
| Live source tab | ✅ PASS |  |
| Archive source tab | ✅ PASS |  |
| YouTube source tab | ✅ PASS |  |
| Spotify source tab | ✅ PASS |  |
| switchRadioSource function | ✅ PASS |  |
| Random station init (not always 0) | ✅ PASS |  |
| lastPlayedStation tracking | ✅ PASS |  |
| Multiple live stations (17+) | ✅ PASS |  |
| Archive collections defined | ✅ PASS |  |
| loadArchivePlaylist function | ✅ PASS |  |
| Archive auto-advance | ✅ PASS |  |
| Progress bar | ✅ PASS |  |
| Seek function | ✅ PASS |  |
| YouTube playlist map | ✅ PASS |  |
| Spotify playlist map | ✅ PASS |  |
| Stream error retry logic | ✅ PASS |  |
| Auto-skip on error | ✅ PASS |  |
| Member portal radio section | ✅ PASS |  |
| Member play/skip controls | ✅ PASS |  |
| Dynamic member schedule list | ✅ PASS |  |
| Admin radio section | ✅ PASS |  |
| Song request form | ✅ PASS |  |

## ✅ Membership (7/7 — 100%)

| Test | Status | Detail |
|------|--------|--------|
| Family tier | ✅ PASS |  |
| Individual tier | ✅ PASS |  |
| Couple tier | ✅ PASS |  |
| Student tier present | ✅ PASS |  |
| Early bird pricing | ✅ PASS |  |
| Registration form exists | ✅ PASS |  |
| Payment method (Zelle) | ✅ PASS |  |

## ✅ Events & Gallery (6/6 — 100%)

| Test | Status | Detail |
|------|--------|--------|
| Events section exists | ✅ PASS |  |
| Durga Puja event | ✅ PASS |  |
| Event cards/list | ✅ PASS |  |
| Gallery section exists | ✅ PASS |  |
| Gallery images | ✅ PASS |  |
| Calendar component | ✅ PASS |  |

## ✅ Admin Dashboard (9/9 — 100%)

| Test | Status | Detail |
|------|--------|--------|
| Admin: Admin Members | ✅ PASS |  |
| Admin: Admin Events | ✅ PASS |  |
| Admin: Admin Radio | ✅ PASS |  |
| Admin: Admin Finance | ✅ PASS |  |
| Admin: Admin Magazine | ✅ PASS |  |
| Admin: Admin Settings | ✅ PASS |  |
| Admin login/auth | ✅ PASS |  |
| Admin navigation | ✅ PASS |  |
| Permission system | ✅ PASS |  |

## ✅ Database Migration (24/24 — 100%)

| Test | Status | Detail |
|------|--------|--------|
| Database file exists | ✅ PASS |  |
| Tables created (44 found) | ✅ PASS | Expected 40+, got 44 |
| Table: persons (416 rows) | ✅ PASS | Expected ≥400 |
| Table: sem_memberships (886 rows) | ✅ PASS | Expected ≥800 |
| Table: sem_families (105 rows) | ✅ PASS | Expected ≥80 |
| Table: sem_events (24 rows) | ✅ PASS | Expected ≥20 |
| Table: transactions (1,085 rows) | ✅ PASS | Expected ≥500 |
| Table: person_roles (899 rows) | ✅ PASS | Expected ≥100 |
| Table: person_relationships (421 rows) | ✅ PASS | Expected ≥200 |
| Table: sem_magazine_contributions (46 rows) | ✅ PASS | Expected ≥30 |
| Table: sem_magazine_advertisements (22 rows) | ✅ PASS | Expected ≥15 |
| Table: organizations (17 rows) | ✅ PASS | Expected ≥10 |
| Table: budgets (17 rows) | ✅ PASS | Expected ≥10 |
| Table: sem_sponsorship_packages (11 rows) | ✅ PASS | Expected ≥5 |
| Membership linking rate: 100.0% | ✅ PASS | 886/886 linked |
| Person-family linking: 54.6% | ✅ PASS | 227/416 |
| EC officers recorded: 10 | ✅ PASS |  |
| Fiscal years with data: 2 | ✅ PASS |  |
|   FY cross_term: 806 members, $0 | ✅ PASS |  |
|   FY 2025-26: 80 members, $23,885 | ✅ PASS |  |
| Unique members: 243 | ✅ PASS |  |
| Distinct events: 9 | ✅ PASS |  |
| Largest family:  (36 members) | ✅ PASS |  |
| Total rows across all tables: 6,915 | ✅ PASS |  |

## ✅ Insight Report (10/10 — 100%)

| Test | Status | Detail |
|------|--------|--------|
| Insight report file exists | ✅ PASS |  |
| Report size (11,052 chars) | ✅ PASS |  |
| Has Executive Summary | ✅ PASS |  |
| Has Demographics section | ✅ PASS |  |
| Has Membership Analysis | ✅ PASS |  |
| Has Governance section | ✅ PASS |  |
| Has Events section | ✅ PASS |  |
| Has Financial section | ✅ PASS |  |
| Has Data Quality section | ✅ PASS |  |
| Has Recommendations | ✅ PASS |  |

## ✅ Mobile Responsiveness (14/14 — 100%)

| Test | Status | Detail |
|------|--------|--------|
| Viewport meta tag | ✅ PASS |  |
| Width=device-width | ✅ PASS |  |
| User-scalable=yes | ✅ PASS |  |
| Maximum-scale >= 3 | ✅ PASS |  |
| Touch-action: pan-y | ✅ PASS |  |
| Webkit overflow scrolling | ✅ PASS |  |
| No dragstart handler on body | ✅ PASS |  |
| No selectstart handler on body | ✅ PASS |  |
| Media query: max-width: 576px | ✅ PASS |  |
| Media query: max-width: 768px | ✅ PASS |  |
| Media query: max-width: 992px | ✅ PASS |  |
| Mobile radio player styles | ✅ PASS |  |
| Mobile schedule chip styles | ✅ PASS |  |
| Form inputs have user-select: text | ✅ PASS |  |

## ✅ JavaScript (23/23 — 100%)

| Test | Status | Detail |
|------|--------|--------|
| Function: toggleRadio() | ✅ PASS |  |
| Function: skipStation() | ✅ PASS |  |
| Function: playScheduleSlot() | ✅ PASS |  |
| Function: switchRadioSource() | ✅ PASS |  |
| Function: buildScheduleStrip() | ✅ PASS |  |
| Function: getCurrentScheduleSlot() | ✅ PASS |  |
| Function: playLiveByCategory() | ✅ PASS |  |
| Function: playArchiveByCategory() | ✅ PASS |  |
| Function: loadArchivePlaylist() | ✅ PASS |  |
| Function: showYouTubeEmbed() | ✅ PASS |  |
| Function: showSpotifyEmbed() | ✅ PASS |  |
| Function: discoverLiveStations() | ✅ PASS |  |
| Function: initRadioPlayer() | ✅ PASS |  |
| Function: updateNowPlaying() | ✅ PASS |  |
| Function: updatePlayButton() | ✅ PASS |  |
| Function: seekRadio() | ✅ PASS |  |
| Function: handleSongRequest() | ✅ PASS |  |
| Navigation: showPortalSection | ✅ PASS |  |
| Navigation: showAdminSection | ✅ PASS |  |
| Navigation: openAdminLoginModal | ✅ PASS |  |
| Navigation: openMemberPortal | ✅ PASS |  |
| No unclosed template literals | ✅ PASS |  |
| DOMContentLoaded listener | ✅ PASS |  |

## ✅ Accessibility (7/7 — 100%)

| Test | Status | Detail |
|------|--------|--------|
| Has <title> tag | ✅ PASS |  |
| Has lang attribute | ✅ PASS |  |
| Images have alt text | ✅ PASS |  |
| Buttons have title/aria | ✅ PASS |  |
| Skip to content link | ✅ PASS |  |
| Form labels present | ✅ PASS |  |
| Required fields marked | ✅ PASS |  |

---

## Recommendations

### Deployment Checklist

- [ ] All 179 tests passing (179 currently pass)
- [ ] Radio station switching works (prev/next/schedule)
- [ ] Mobile scrolling verified on real device
- [ ] GitHub Pages deployment updated
- [ ] Database migration verified (banf_archive.db)
- [ ] Insight report accessible

---

*Report generated by BANF Comprehensive Test Suite v1.0*
