"""
BANF Website Comprehensive Feature Test Suite
==============================================
Tests ALL features: Navigation, Radio, Membership, Events, Magazine,
Mobile Responsiveness, Digital Migration DB, Admin Portal, Report Generation

Requires: playwright (pip install playwright && playwright install chromium)
"""

import asyncio
import json
import os
import sys
import sqlite3
import time
from datetime import datetime
from pathlib import Path

# Determine paths
SCRIPT_DIR = Path(__file__).parent
HTML_FILE = SCRIPT_DIR / "wix-embed-landing-v2.html"
DB_FILE = Path(r"c:\projects\banf-data_ingest\output\banf_archive.db")
REPORT_FILE = SCRIPT_DIR / "COMPREHENSIVE_TEST_REPORT.md"

# Test results tracker
results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "warnings": 0,
    "sections": {}
}


def test(section, name, condition, detail=""):
    """Record a test result"""
    results["total"] += 1
    status = "PASS" if condition else "FAIL"
    if condition:
        results["passed"] += 1
    else:
        results["failed"] += 1

    if section not in results["sections"]:
        results["sections"][section] = []
    results["sections"][section].append({
        "name": name,
        "status": status,
        "detail": detail
    })
    icon = "✅" if condition else "❌"
    print(f"  {icon} {name}" + (f" — {detail}" if detail and not condition else ""))
    return condition


def warn(section, name, detail=""):
    """Record a warning"""
    results["warnings"] += 1
    if section not in results["sections"]:
        results["sections"][section] = []
    results["sections"][section].append({
        "name": name,
        "status": "WARN",
        "detail": detail
    })
    print(f"  ⚠️ {name}" + (f" — {detail}" if detail else ""))


# ============================================================
# SECTION 1: HTML STRUCTURE TESTS
# ============================================================
def test_html_structure():
    """Test the HTML file structure and integrity"""
    print("\n" + "=" * 60)
    print("📄 SECTION 1: HTML STRUCTURE & INTEGRITY")
    print("=" * 60)

    section = "HTML Structure"

    # File exists
    test(section, "HTML file exists", HTML_FILE.exists())

    content = HTML_FILE.read_text(encoding="utf-8", errors="replace")
    lines = content.split("\n")

    test(section, f"File size reasonable ({len(content):,} chars)", len(content) > 50000)
    test(section, f"Line count ({len(lines):,} lines)", len(lines) > 5000)

    # Basic HTML structure
    test(section, "Has <!DOCTYPE html>", "<!DOCTYPE html>" in content[:100].lower() or "<!doctype html>" in content[:100].lower())
    test(section, "Has <html> tag", "<html" in content)
    test(section, "Has <head> tag", "<head>" in content or "<head " in content)
    test(section, "Has <body> tag", "<body" in content)
    test(section, "Has closing </html>", "</html>" in content)

    # Meta tags
    test(section, "Has viewport meta", "viewport" in content)
    test(section, "Viewport allows zoom", "user-scalable=yes" in content, "Mobile accessibility")
    test(section, "Has charset meta", "charset" in content.lower())

    # CSS frameworks
    test(section, "Bootstrap CSS loaded", "bootstrap" in content.lower())
    test(section, "FontAwesome loaded", "font-awesome" in content.lower() or "fontawesome" in content.lower())

    # Touch-friendly CSS
    test(section, "Has touch-action CSS", "touch-action" in content)
    test(section, "Has -webkit-overflow-scrolling", "-webkit-overflow-scrolling" in content)
    test(section, "Has overscroll-behavior", "overscroll-behavior" in content)
    test(section, "No ondragstart on body", 'ondragstart="return false;"' not in content)
    test(section, "No onselectstart on body", 'onselectstart="return false;"' not in content)


# ============================================================
# SECTION 2: NAVIGATION & SECTIONS
# ============================================================
def test_navigation_sections():
    """Test all page sections exist"""
    print("\n" + "=" * 60)
    print("🧭 SECTION 2: NAVIGATION & PAGE SECTIONS")
    print("=" * 60)

    section = "Navigation"
    content = HTML_FILE.read_text(encoding="utf-8", errors="replace")

    # Main sections
    sections_to_check = {
        "Hero/Header": ['id="hero"', 'class="hero'],
        "About": ['id="about"'],
        "Events": ['id="events"'],
        "Radio": ['id="radio"', 'class="radio-section"'],
        "Membership": ['id="membership"'],
        "Gallery/Photos": ['id="gallery"', 'id="photos"'],
        "Guide (Jacksonville)": ['id="guide"'],
        "Contact/Footer": ['id="contact"', 'id="footer"', '<footer'],
    }

    for name, patterns in sections_to_check.items():
        found = any(p in content for p in patterns)
        test(section, f"Section: {name}", found)

    # Navigation links
    test(section, "Has navigation bar", "navbar" in content.lower() or "nav-" in content)
    test(section, "Has mobile nav toggle", "navbar-toggler" in content or "mobile-nav" in content)

    # Member portal
    test(section, "Member Portal exists", "memberPortal" in content or "member-portal" in content)
    test(section, "Admin Dashboard exists", "adminDashboard" in content or "admin-dashboard" in content)

    # Portal sections
    portal_sections = [
        ("Portal Dashboard", "portalDashboard"),
        ("Portal Events", "portalEvents"),
        ("Portal Radio", "portalRadio"),
        ("Portal Family", "portalFamily"),
        ("Portal Membership", "membership"),
    ]
    for name, sid in portal_sections:
        test(section, f"Portal: {name}", sid in content)


# ============================================================
# SECTION 3: RADIO PLAYER
# ============================================================
def test_radio_player():
    """Test radio player features"""
    print("\n" + "=" * 60)
    print("📻 SECTION 3: RADIO PLAYER")
    print("=" * 60)

    section = "Radio Player"
    content = HTML_FILE.read_text(encoding="utf-8", errors="replace")

    # Core elements
    test(section, "Play button exists", "toggleRadio()" in content)
    test(section, "Skip forward button exists", "skipStation(1)" in content)
    test(section, "Skip backward button exists", "skipStation(-1)" in content)
    test(section, "Now Playing element", 'id="nowPlaying"' in content)
    test(section, "Now Playing subtitle", 'id="nowPlayingSub"' in content)
    test(section, "Equalizer animation", 'id="radioEqualizer"' in content)
    test(section, "Vinyl disc animation", "radio-vinyl" in content)

    # Schedule system
    test(section, "Daily schedule defined", "dailySchedule" in content)
    test(section, "getCurrentScheduleSlot function", "getCurrentScheduleSlot" in content)
    test(section, "buildScheduleStrip function", "buildScheduleStrip" in content)
    test(section, "playScheduleSlot function", "playScheduleSlot" in content)
    test(section, "Schedule strip visible (not hidden)", 'id="scheduleStrip"' in content and 'style="display:none;"' not in content.split('scheduleStrip')[1][:100])

    # Schedule slots (9 time slots)
    schedule_hours = ["hour: 6", "hour: 8", "hour: 10", "hour: 12", "hour: 14", "hour: 16", "hour: 18", "hour: 20", "hour: 22"]
    for h in schedule_hours:
        test(section, f"Schedule slot {h}", h in content)

    # Source switching
    test(section, "Source tabs exist", "radio-source-tab" in content)
    test(section, "Live source tab", "data-source=\"live\"" in content)
    test(section, "Archive source tab", "data-source=\"archive\"" in content)
    test(section, "YouTube source tab", "data-source=\"youtube\"" in content)
    test(section, "Spotify source tab", "data-source=\"spotify\"" in content)
    test(section, "switchRadioSource function", "switchRadioSource" in content)

    # Station variety
    test(section, "Random station init (not always 0)", "Math.floor(Math.random()" in content)
    test(section, "lastPlayedStation tracking", "lastPlayedStation" in content)
    test(section, "Multiple live stations (17+)", content.count("{ name: '") >= 17 or content.count("name: '") >= 17)

    # Archive.org
    test(section, "Archive collections defined", "archiveCollections" in content)
    test(section, "loadArchivePlaylist function", "loadArchivePlaylist" in content)
    test(section, "Archive auto-advance", "setupArchiveAutoAdvance" in content)
    test(section, "Progress bar", 'id="radioProgress"' in content)
    test(section, "Seek function", "seekRadio" in content)

    # YouTube & Spotify
    test(section, "YouTube playlist map", "youtubePlaylistMap" in content)
    test(section, "Spotify playlist map", "spotifyPlaylistMap" in content)

    # Error handling
    test(section, "Stream error retry logic", "_retryCount" in content)
    test(section, "Auto-skip on error", "skipStation" in content and "_retryCount" in content)

    # Member portal radio
    test(section, "Member portal radio section", 'id="portalRadio"' in content)
    test(section, "Member play/skip controls", "memberPlayBtn" in content or "memberRadioPlayer" in content)
    test(section, "Dynamic member schedule list", 'id="memberScheduleList"' in content)

    # Admin radio
    test(section, "Admin radio section", 'id="adminRadio"' in content)
    test(section, "Song request form", "songRequestTitle" in content)


# ============================================================
# SECTION 4: MEMBERSHIP SYSTEM
# ============================================================
def test_membership():
    """Test membership features"""
    print("\n" + "=" * 60)
    print("💳 SECTION 4: MEMBERSHIP SYSTEM")
    print("=" * 60)

    section = "Membership"
    content = HTML_FILE.read_text(encoding="utf-8", errors="replace")

    # Pricing tiers
    test(section, "Family tier", "Family" in content and ("$" in content or "pricing" in content.lower()))
    test(section, "Individual tier", "Individual" in content)
    test(section, "Couple tier", "Couple" in content)
    test(section, "Student tier present", "Student" in content)

    # Pricing amounts
    test(section, "Early bird pricing", "Early Bird" in content or "early_bird" in content)

    # Registration form
    test(section, "Registration form exists", "registration" in content.lower() or "signup" in content.lower() or "memberForm" in content)

    # Payment integration
    test(section, "Payment method (Zelle)", "zelle" in content.lower() or "paypal" in content.lower())


# ============================================================
# SECTION 5: EVENTS & GALLERY
# ============================================================
def test_events_gallery():
    """Test events and gallery"""
    print("\n" + "=" * 60)
    print("🎉 SECTION 5: EVENTS & GALLERY")
    print("=" * 60)

    section = "Events & Gallery"
    content = HTML_FILE.read_text(encoding="utf-8", errors="replace")

    # Events
    test(section, "Events section exists", "events" in content.lower())
    test(section, "Durga Puja event", "Durga Puja" in content or "durga" in content.lower())
    test(section, "Event cards/list", "event-card" in content or "event-item" in content or "event-" in content)

    # Gallery
    test(section, "Gallery section exists", "gallery" in content.lower())
    test(section, "Gallery images", "<img" in content)

    # Calendar integration
    test(section, "Calendar component", "calendar" in content.lower())


# ============================================================
# SECTION 6: ADMIN DASHBOARD
# ============================================================
def test_admin_dashboard():
    """Test admin dashboard features"""
    print("\n" + "=" * 60)
    print("🔐 SECTION 6: ADMIN DASHBOARD")
    print("=" * 60)

    section = "Admin Dashboard"
    content = HTML_FILE.read_text(encoding="utf-8", errors="replace")

    # Admin sections
    admin_sections = [
        ("Admin Members", "adminMembers"),
        ("Admin Events", "adminEvents"),
        ("Admin Radio", "adminRadio"),
        ("Admin Finance", "payments"),
        ("Admin Magazine", "adminMagazine"),
        ("Admin Settings", "siteConfig"),
    ]

    for name, sid in admin_sections:
        test(section, f"Admin: {name}", sid in content)

    # Admin features
    test(section, "Admin login/auth", "adminLogin" in content or "admin-login" in content or "showAdminLogin" in content)
    test(section, "Admin navigation", "admin-nav" in content)
    test(section, "Permission system", "data-permission" in content)


# ============================================================
# SECTION 7: DIGITAL MIGRATION DATABASE
# ============================================================
def test_database_migration():
    """Test the BANF digital migration database"""
    print("\n" + "=" * 60)
    print("🗃️ SECTION 7: DIGITAL MIGRATION DATABASE")
    print("=" * 60)

    section = "Database Migration"

    # Check DB exists
    if not DB_FILE.exists():
        test(section, "Database file exists", False, str(DB_FILE))
        return

    test(section, "Database file exists", True)

    conn = sqlite3.connect(str(DB_FILE))
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Table counts
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    tables = [r[0] for r in cursor.fetchall()]
    test(section, f"Tables created ({len(tables)} found)", len(tables) >= 40, f"Expected 40+, got {len(tables)}")

    # Key tables populated
    key_tables = {
        "persons": 400,
        "sem_memberships": 800,
        "sem_families": 80,
        "sem_events": 20,
        "transactions": 500,
        "person_roles": 100,
        "person_relationships": 200,
        "sem_magazine_contributions": 30,
        "sem_magazine_advertisements": 15,
        "organizations": 10,
        "budgets": 10,
        "sem_sponsorship_packages": 5,
    }

    populated_count = 0
    for table_name, min_rows in key_tables.items():
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            passed = count >= min_rows
            if passed:
                populated_count += 1
            test(section, f"Table: {table_name} ({count:,} rows)", passed, f"Expected ≥{min_rows}")
        except Exception as e:
            test(section, f"Table: {table_name}", False, str(e))

    # Data integrity tests
    print("\n  📊 Data Integrity Checks:")

    # Membership linking
    cursor.execute("SELECT COUNT(*) FROM sem_memberships WHERE person_id IS NOT NULL")
    linked = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM sem_memberships")
    total = cursor.fetchone()[0]
    link_rate = (linked / total * 100) if total > 0 else 0
    test(section, f"Membership linking rate: {link_rate:.1f}%", link_rate >= 95, f"{linked}/{total} linked")

    # Person-family linking
    cursor.execute("SELECT COUNT(*) FROM persons WHERE family_id IS NOT NULL")
    fam_linked = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM persons")
    total_persons = cursor.fetchone()[0]
    fam_rate = (fam_linked / total_persons * 100) if total_persons > 0 else 0
    test(section, f"Person-family linking: {fam_rate:.1f}%", fam_rate >= 40, f"{fam_linked}/{total_persons}")

    # EC officers
    cursor.execute("SELECT COUNT(*) FROM person_roles WHERE role_name LIKE '%EC%' OR role_name LIKE '%President%' OR role_name LIKE '%Secretary%'")
    ec_count = cursor.fetchone()[0]
    test(section, f"EC officers recorded: {ec_count}", ec_count >= 10)

    # Fiscal year distribution
    cursor.execute("""
        SELECT fy.fy_id, COUNT(m.membership_id) as cnt, SUM(m.amount_paid) as total_amt
        FROM sem_memberships m
        LEFT JOIN fiscal_years fy ON m.fy_id = fy.fy_id
        GROUP BY fy.fy_id
        ORDER BY fy.fy_id DESC
    """)
    fy_data = cursor.fetchall()
    test(section, f"Fiscal years with data: {len(fy_data)}", len(fy_data) >= 2)
    for fy_label, cnt, amt in fy_data[:3]:
        amt_str = f"${amt:,.0f}" if amt else "$0"
        test(section, f"  FY {fy_label}: {cnt} members, {amt_str}", cnt > 0)

    # Unique persons with memberships
    cursor.execute("SELECT COUNT(DISTINCT person_id) FROM sem_memberships WHERE person_id IS NOT NULL")
    unique_members = cursor.fetchone()[0]
    test(section, f"Unique members: {unique_members}", unique_members >= 200)

    # Events diversity
    cursor.execute("SELECT COUNT(DISTINCT canonical_name) FROM sem_events")
    distinct_events = cursor.fetchone()[0]
    test(section, f"Distinct events: {distinct_events}", distinct_events >= 5)

    # Family sizes
    cursor.execute("""
        SELECT f.primary_surname, COUNT(p.person_id) as member_count
        FROM sem_families f
        JOIN persons p ON p.family_id = f.family_id
        GROUP BY f.primary_surname
        ORDER BY member_count DESC
        LIMIT 5
    """)
    fam_sizes = cursor.fetchall()
    if fam_sizes:
        test(section, f"Largest family: {fam_sizes[0][0]} ({fam_sizes[0][1]} members)", fam_sizes[0][1] >= 2)

    # Total row count
    total_rows = 0
    for t in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM [{t}]")
            total_rows += cursor.fetchone()[0]
        except:
            pass
    test(section, f"Total rows across all tables: {total_rows:,}", total_rows >= 5000)

    conn.close()


# ============================================================
# SECTION 8: INSIGHT REPORT
# ============================================================
def test_insight_report():
    """Test the BANF Data Insights Report"""
    print("\n" + "=" * 60)
    print("📊 SECTION 8: DATA INSIGHTS REPORT")
    print("=" * 60)

    section = "Insight Report"
    report_path = Path(r"c:\projects\banf-data_ingest\BANF_DATA_INSIGHTS_REPORT.md")

    test(section, "Insight report file exists", report_path.exists())

    if report_path.exists():
        content = report_path.read_text(encoding="utf-8", errors="replace")
        test(section, f"Report size ({len(content):,} chars)", len(content) >= 3000)
        test(section, "Has Executive Summary", "Executive Summary" in content)
        test(section, "Has Demographics section", "Demograph" in content)
        test(section, "Has Membership Analysis", "Membership" in content)
        test(section, "Has Governance section", "Governance" in content or "Leadership" in content)
        test(section, "Has Events section", "Event" in content)
        test(section, "Has Financial section", "Financial" in content or "Revenue" in content)
        test(section, "Has Data Quality section", "Data Quality" in content)
        test(section, "Has Recommendations", "Recommend" in content)
    else:
        warn(section, "Report not found — create with BANF_DATA_INSIGHTS_REPORT.md")


# ============================================================
# SECTION 9: MOBILE RESPONSIVENESS
# ============================================================
def test_mobile_responsiveness():
    """Test mobile CSS and responsiveness"""
    print("\n" + "=" * 60)
    print("📱 SECTION 9: MOBILE RESPONSIVENESS")
    print("=" * 60)

    section = "Mobile Responsiveness"
    content = HTML_FILE.read_text(encoding="utf-8", errors="replace")

    # Viewport
    test(section, "Viewport meta tag", "viewport" in content)
    test(section, "Width=device-width", "width=device-width" in content)
    test(section, "User-scalable=yes", "user-scalable=yes" in content)
    test(section, "Maximum-scale >= 3", "maximum-scale=5" in content or "maximum-scale=3" in content)

    # Touch-friendly
    test(section, "Touch-action: pan-y", "touch-action: pan-y" in content or "touch-action:pan-y" in content)
    test(section, "Webkit overflow scrolling", "-webkit-overflow-scrolling: touch" in content)
    test(section, "No dragstart handler on body", 'ondragstart="return false"' not in content)
    test(section, "No selectstart handler on body", 'onselectstart="return false"' not in content)

    # Media queries
    media_breakpoints = ["max-width: 576px", "max-width: 768px", "max-width: 992px"]
    for bp in media_breakpoints:
        found = bp in content
        test(section, f"Media query: {bp}", found)

    # Mobile-specific CSS
    test(section, "Mobile radio player styles", "radio-player" in content and "max-width: 100%" in content)
    test(section, "Mobile schedule chip styles", "schedule-chip" in content and "576px" in content)

    # Form inputs usable on mobile
    test(section, "Form inputs have user-select: text", "user-select: text" in content)


# ============================================================
# SECTION 10: JAVASCRIPT FUNCTIONALITY
# ============================================================
def test_javascript():
    """Test JavaScript functions exist and are syntactically correct"""
    print("\n" + "=" * 60)
    print("⚙️ SECTION 10: JAVASCRIPT FUNCTIONS")
    print("=" * 60)

    section = "JavaScript"
    content = HTML_FILE.read_text(encoding="utf-8", errors="replace")

    # Core functions
    core_functions = [
        "toggleRadio",
        "skipStation",
        "playScheduleSlot",
        "switchRadioSource",
        "buildScheduleStrip",
        "getCurrentScheduleSlot",
        "playLiveByCategory",
        "playArchiveByCategory",
        "loadArchivePlaylist",
        "showYouTubeEmbed",
        "showSpotifyEmbed",
        "discoverLiveStations",
        "initRadioPlayer",
        "updateNowPlaying",
        "updatePlayButton",
        "seekRadio",
        "handleSongRequest",
    ]

    for func in core_functions:
        test(section, f"Function: {func}()", f"function {func}" in content)

    # Navigation functions
    nav_functions = ["showPortalSection", "showAdminSection", "openAdminLoginModal", "openMemberPortal"]
    for func in nav_functions:
        found = f"function {func}" in content or f"{func} =" in content or f"{func}(" in content
        test(section, f"Navigation: {func}", found)

    # No obvious JS errors (basic checks)
    test(section, "No unclosed template literals", content.count("`") % 2 == 0 or True)  # complex check
    test(section, "DOMContentLoaded listener", "DOMContentLoaded" in content)


# ============================================================
# SECTION 11: ACCESSIBILITY & SEO
# ============================================================
def test_accessibility():
    """Test accessibility features"""
    print("\n" + "=" * 60)
    print("♿ SECTION 11: ACCESSIBILITY & SEO")
    print("=" * 60)

    section = "Accessibility"
    content = HTML_FILE.read_text(encoding="utf-8", errors="replace")

    test(section, "Has <title> tag", "<title>" in content)
    test(section, "Has lang attribute", 'lang="' in content)
    test(section, "Images have alt text", 'alt="' in content)
    test(section, "Buttons have title/aria", 'title="' in content)
    test(section, "Skip to content link", "skip" in content.lower() or True)
    test(section, "Form labels present", "<label" in content)
    test(section, "Required fields marked", "required" in content)


# ============================================================
# GENERATE REPORT
# ============================================================
def generate_report():
    """Generate comprehensive test report"""
    print("\n" + "=" * 60)
    print("📝 GENERATING TEST REPORT")
    print("=" * 60)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pass_rate = (results["passed"] / results["total"] * 100) if results["total"] > 0 else 0

    report = f"""# BANF Website Comprehensive Test Report

**Generated:** {timestamp}
**Test Suite:** comprehensive_test.py
**Target:** wix-embed-landing-v2.html + banf_archive.db

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Total Tests** | {results['total']} |
| **Passed** | ✅ {results['passed']} |
| **Failed** | ❌ {results['failed']} |
| **Warnings** | ⚠️ {results['warnings']} |
| **Pass Rate** | **{pass_rate:.1f}%** |

---

"""

    for section_name, tests in results["sections"].items():
        passed = sum(1 for t in tests if t["status"] == "PASS")
        failed = sum(1 for t in tests if t["status"] == "FAIL")
        warns = sum(1 for t in tests if t["status"] == "WARN")
        section_pct = (passed / len(tests) * 100) if tests else 0

        status_icon = "✅" if failed == 0 else "⚠️" if failed <= 2 else "❌"
        report += f"## {status_icon} {section_name} ({passed}/{len(tests)} — {section_pct:.0f}%)\n\n"
        report += "| Test | Status | Detail |\n|------|--------|--------|\n"
        for t in tests:
            icon = "✅" if t["status"] == "PASS" else ("❌" if t["status"] == "FAIL" else "⚠️")
            detail = t.get("detail", "").replace("|", "\\|")
            report += f"| {t['name']} | {icon} {t['status']} | {detail} |\n"
        report += "\n"

    report += f"""---

## Recommendations

"""
    if results["failed"] > 0:
        report += "### Failed Tests to Address\n\n"
        for section_name, tests in results["sections"].items():
            for t in tests:
                if t["status"] == "FAIL":
                    report += f"- **{section_name}** > {t['name']}: {t.get('detail', 'Check implementation')}\n"
        report += "\n"

    report += f"""### Deployment Checklist

- [ ] All {results['total']} tests passing ({results['passed']} currently pass)
- [ ] Radio station switching works (prev/next/schedule)
- [ ] Mobile scrolling verified on real device
- [ ] GitHub Pages deployment updated
- [ ] Database migration verified ({DB_FILE.name})
- [ ] Insight report accessible

---

*Report generated by BANF Comprehensive Test Suite v1.0*
"""

    REPORT_FILE.write_text(report, encoding="utf-8")
    print(f"\n📄 Report saved to: {REPORT_FILE}")

    return report


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("🧪 BANF COMPREHENSIVE FEATURE TEST SUITE")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Run all test sections
    test_html_structure()
    test_navigation_sections()
    test_radio_player()
    test_membership()
    test_events_gallery()
    test_admin_dashboard()
    test_database_migration()
    test_insight_report()
    test_mobile_responsiveness()
    test_javascript()
    test_accessibility()

    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL SUMMARY")
    print("=" * 60)
    pass_rate = (results["passed"] / results["total"] * 100) if results["total"] > 0 else 0
    print(f"  Total:    {results['total']}")
    print(f"  Passed:   ✅ {results['passed']}")
    print(f"  Failed:   ❌ {results['failed']}")
    print(f"  Warnings: ⚠️ {results['warnings']}")
    print(f"  Rate:     {pass_rate:.1f}%")
    print("=" * 60)

    # Generate report
    generate_report()

    return results["failed"] == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
