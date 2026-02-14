# -*- coding: utf-8 -*-
"""
BANF Zelle Payment Automation Service
=======================================
Monitors banfjax@gmail.com for Zelle payment notification emails,
parses payment details, and stores them in a local SQLite database.
Auto-updates member payment records when Zelle emails are detected.

Architecture:
  Gmail IMAP → Parse Zelle Email → SQLite DB → REST API → Frontend

Usage:
  python zelle_payment_service.py
  # Runs on http://localhost:5002
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import imaplib
import email
from email.header import decode_header
import sqlite3
import json
import os
import re
import threading
import time
import traceback
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ====== CONFIGURATION ======
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "banfjax@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "skmxlbejaryowvkt")
IMAP_SERVER = "imap.gmail.com"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zelle_payments.db")
POLL_INTERVAL = int(os.getenv("ZELLE_POLL_INTERVAL", "60"))  # seconds

# Zelle email patterns (subjects that indicate Zelle payments)
ZELLE_SUBJECT_PATTERNS = [
    r'(?:You\s+)?(?:received|got)\s+\$[\d,]+(?:\.\d{2})?\s+(?:from|via)\s+',
    r'Zelle\s+(?:payment|transfer)\s+(?:from|received)',
    r'\$[\d,]+(?:\.\d{2})?\s+(?:Zelle|zelle)\s+(?:payment|deposit)',
    r'(?:New\s+)?Zelle\s+(?:payment\s+)?notification',
    r'You\s+(?:have\s+)?received\s+.*\s+through\s+Zelle',
    r'Zelle®?\s*[:,]?\s*(?:You\s+)?(?:received|got)',
    r'payment\s+received\s+via\s+Zelle',
    r'Direct\s+deposit.*Zelle',
    r'Money\s+received.*Zelle',
    # Chase/BofA/Wells Fargo specific patterns
    r'Chase.*Zelle.*received',
    r'Wells\s+Fargo.*Zelle',
    r'Bank\s+of\s+America.*Zelle',
]

# Common Zelle sender email domains (bank notification senders)
ZELLE_SENDER_DOMAINS = [
    'chase.com', 'bankofamerica.com', 'wellsfargo.com',
    'usbank.com', 'pnc.com', 'capitalone.com', 'zellepay.com',
    'notify.zelle.com', 'alerts.chase.com', 'ealerts.bankofamerica.com',
]


# ====== DATABASE SETUP ======

def init_db():
    """Initialize SQLite database with payment tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Zelle payments table
    c.execute('''CREATE TABLE IF NOT EXISTS zelle_payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email_id TEXT UNIQUE,
        email_date TEXT,
        sender_name TEXT,
        sender_email TEXT,
        amount REAL,
        currency TEXT DEFAULT 'USD',
        memo TEXT,
        confirmation_code TEXT,
        bank_source TEXT,
        raw_subject TEXT,
        raw_body_snippet TEXT,
        matched_member_id TEXT,
        matched_member_name TEXT,
        matched_member_email TEXT,
        status TEXT DEFAULT 'pending',
        verified_by TEXT,
        verified_at TEXT,
        auto_matched INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    # Members table (local cache for matching)
    c.execute('''CREATE TABLE IF NOT EXISTS members (
        id TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        membership_type TEXT,
        status TEXT DEFAULT 'active',
        balance_due REAL DEFAULT 0,
        total_paid REAL DEFAULT 0,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    # Payment history (all payment events)
    c.execute('''CREATE TABLE IF NOT EXISTS payment_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT,
        member_name TEXT,
        payment_type TEXT,
        amount REAL,
        description TEXT,
        payment_method TEXT DEFAULT 'Zelle',
        zelle_payment_id INTEGER,
        status TEXT DEFAULT 'completed',
        receipt_number TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (zelle_payment_id) REFERENCES zelle_payments(id)
    )''')

    # Polling log
    c.execute('''CREATE TABLE IF NOT EXISTS poll_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        poll_time TEXT,
        emails_checked INTEGER DEFAULT 0,
        new_payments_found INTEGER DEFAULT 0,
        auto_matched INTEGER DEFAULT 0,
        errors TEXT,
        duration_ms INTEGER
    )''')

    # Settings
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    # Seed demo members if empty
    c.execute("SELECT COUNT(*) FROM members")
    if c.fetchone()[0] == 0:
        demo_members = [
            ('demo_member', 'Test', 'Member', 'Test Member', 'member@test.com', '(904) 555-1234', 'Family', 'active', 0, 250),
            ('demo_admin', 'Admin', 'User', 'Admin User', 'admin@test.com', '(904) 555-9999', 'Family', 'active', 0, 375),
            ('m_banerjee', 'Sunil', 'Banerjee', 'Sunil Banerjee', 'sunil.banerjee@gmail.com', '(904) 555-2001', 'Family', 'active', 150, 0),
            ('m_sen', 'Priya', 'Sen', 'Priya Sen', 'priya.sen@gmail.com', '(904) 555-2002', 'Individual', 'active', 0, 100),
            ('m_roy', 'Amit', 'Roy', 'Amit Roy', 'amit.roy@gmail.com', '(904) 555-2003', 'Family', 'active', 0, 250),
            ('m_das', 'Rina', 'Das', 'Rina Das', 'rina.das@gmail.com', '(904) 555-2004', 'Individual', 'active', 75, 75),
            ('m_ghosh', 'Soham', 'Ghosh', 'Soham Ghosh', 'soham.ghosh@gmail.com', '(904) 555-2005', 'Family', 'active', 0, 375),
            ('m_mukherjee', 'Ananya', 'Mukherjee', 'Ananya Mukherjee', 'ananya.m@gmail.com', '(904) 555-2006', 'Senior', 'active', 50, 50),
        ]
        c.executemany('''INSERT OR IGNORE INTO members
            (id, first_name, last_name, full_name, email, phone, membership_type, status, balance_due, total_paid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', demo_members)

    conn.commit()
    conn.close()
    print(f"[DB] Database initialized: {DB_PATH}")


# ====== EMAIL PARSING ======

def decode_email_header(header_value):
    """Decode email header"""
    if not header_value:
        return ""
    decoded_parts = decode_header(header_value)
    result = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            result += part.decode(encoding or 'utf-8', errors='replace')
        else:
            result += str(part)
    return result


def is_zelle_email(subject, from_addr, body=""):
    """Check if an email is a Zelle payment notification"""
    text = f"{subject} {from_addr} {body}".lower()

    # Check subject patterns
    for pattern in ZELLE_SUBJECT_PATTERNS:
        if re.search(pattern, subject, re.IGNORECASE):
            return True

    # Check sender domain
    for domain in ZELLE_SENDER_DOMAINS:
        if domain.lower() in from_addr.lower():
            if 'zelle' in text:
                return True

    # Fallback: check if 'zelle' + money pattern in combined text
    if 'zelle' in text and re.search(r'\$[\d,]+(?:\.\d{2})?', text):
        return True

    return False


def parse_zelle_amount(text):
    """Extract dollar amount from text"""
    patterns = [
        r'\$\s*([\d,]+(?:\.\d{2})?)',       # $150.00 or $1,500.00
        r'([\d,]+(?:\.\d{2})?)\s*(?:USD|dollars?)',  # 150.00 USD
        r'amount[:\s]*\$?\s*([\d,]+(?:\.\d{2})?)',   # amount: $150
        r'received[:\s]*\$?\s*([\d,]+(?:\.\d{2})?)',  # received $150
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(',', '')
            try:
                return float(amount_str)
            except ValueError:
                continue
    return None


def parse_zelle_sender(subject, body):
    """Extract sender name from Zelle email"""
    patterns = [
        r'from\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})',  # "from John Smith"
        r'([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})\s+sent\s+you',  # "John Smith sent you"
        r'(?:sent|paid)\s+by\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})',  # "paid by John"
        r'Zelle.*?from\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,3})',
    ]
    combined = f"{subject}\n{body}"
    for pattern in patterns:
        match = re.search(pattern, combined)
        if match:
            name = match.group(1).strip()
            # Filter out common false positives
            noise = {'Zelle', 'Chase', 'Wells', 'Fargo', 'Bank', 'America', 'Direct', 'Deposit', 'Payment', 'Your', 'The'}
            if name.split()[0] not in noise:
                return name
    return "Unknown Sender"


def parse_zelle_memo(body):
    """Extract memo/note from Zelle email body"""
    patterns = [
        r'(?:memo|note|message|description)[:\s]*[""]?([^""\n]{3,80})[""]?',
        r'(?:for|regarding)[:\s]*[""]?([^""\n]{3,80})[""]?',
        r'Membership\s*[-–]\s*([A-Z][a-zA-Z\s]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


def parse_zelle_confirmation(body):
    """Extract confirmation/reference code"""
    patterns = [
        r'(?:confirmation|reference|transaction|ref)\s*(?:#|number|code|id)?[:\s]*([A-Z0-9]{6,20})',
        r'(?:ID|Id)[:\s]*([A-Z0-9]{6,20})',
    ]
    for pattern in patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


def parse_bank_source(from_addr, body):
    """Identify which bank sent the notification"""
    text = f"{from_addr} {body}".lower()
    bank_map = {
        'chase': 'Chase',
        'bankofamerica': 'Bank of America',
        'wellsfargo': 'Wells Fargo',
        'usbank': 'US Bank',
        'pnc': 'PNC',
        'capitalone': 'Capital One',
        'zelle': 'Zelle Direct',
    }
    for key, name in bank_map.items():
        if key in text:
            return name
    return "Unknown Bank"


def get_email_body(msg):
    """Extract text body from email message"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    body = payload.decode(charset, errors='replace')
                    break
            elif ctype == 'text/html' and not body:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    html = payload.decode(charset, errors='replace')
                    # Strip HTML tags for parsing
                    body = re.sub(r'<[^>]+>', ' ', html)
                    body = re.sub(r'\s+', ' ', body).strip()
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or 'utf-8'
            body = payload.decode(charset, errors='replace')
    return body[:5000]  # Limit to 5KB


# ====== MEMBER MATCHING ======

def match_member(sender_name, memo, amount, sender_email=""):
    """Try to auto-match a Zelle payment to a member"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Strategy 1: Match by email (strongest signal)
    if sender_email:
        c.execute("SELECT * FROM members WHERE LOWER(email) = LOWER(?)", (sender_email,))
        member = c.fetchone()
        if member:
            conn.close()
            return dict(member), 'email_match'

    # Strategy 2: Match by name in memo (e.g., "Membership - Sunil Banerjee")
    if memo:
        c.execute("SELECT * FROM members")
        for m in c.fetchall():
            m = dict(m)
            full = m['full_name'].lower()
            last = m['last_name'].lower()
            if full in memo.lower() or last in memo.lower():
                conn.close()
                return m, 'memo_match'

    # Strategy 3: Match by sender name
    if sender_name and sender_name != "Unknown Sender":
        name_lower = sender_name.lower()
        c.execute("SELECT * FROM members")
        for m in c.fetchall():
            m = dict(m)
            full = m['full_name'].lower()
            last = m['last_name'].lower()
            first = m['first_name'].lower()
            # Exact match
            if name_lower == full:
                conn.close()
                return m, 'name_exact'
            # Last name match
            if last in name_lower or name_lower in full:
                conn.close()
                return m, 'name_partial'

    conn.close()
    return None, 'no_match'


# ====== GMAIL POLLING ======

def poll_gmail_for_zelle(days_back=30, force_full_scan=False):
    """
    Poll Gmail inbox for Zelle payment emails.
    Returns dict with results summary.
    """
    start_time = time.time()
    results = {
        'emails_checked': 0,
        'new_payments': 0,
        'auto_matched': 0,
        'errors': [],
        'payments': []
    }

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        mail.select("INBOX", readonly=True)
    except Exception as conn_err:
        results['errors'].append(f"Gmail connection failed: {str(conn_err)}")
        print(f"[SCAN] Gmail connection failed: {conn_err}")
        return results

    try:
        since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")

        # Search for emails with Zelle-related terms
        search_criteria = f'(OR (SUBJECT "Zelle") (SUBJECT "zelle") (SUBJECT "received") (BODY "Zelle") SINCE {since_date})'
        try:
            status, msg_ids = mail.search(None, search_criteria)
        except Exception:
            # Fallback: simpler search
            status, msg_ids = mail.search(None, f'SINCE {since_date}')

        if status != 'OK' or not msg_ids[0]:
            mail.logout()
            return results

        email_ids = msg_ids[0].split()
        results['emails_checked'] = len(email_ids)

        # Get existing email IDs to skip duplicates
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT email_id FROM zelle_payments")
        existing_ids = {row[0] for row in c.fetchall()}
        conn.close()

        for eid in email_ids:
            try:
                eid_str = eid.decode() if isinstance(eid, bytes) else str(eid)

                # Skip if already processed
                if eid_str in existing_ids:
                    continue

                status, msg_data = mail.fetch(eid, "(RFC822)")
                if status != 'OK':
                    continue

                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                subject = decode_email_header(msg.get("Subject", ""))
                from_addr = decode_email_header(msg.get("From", ""))
                date_str = msg.get("Date", "")
                body = get_email_body(msg)

                # Check if this is a Zelle email
                if not is_zelle_email(subject, from_addr, body):
                    continue

                # Parse payment details
                amount = parse_zelle_amount(f"{subject} {body}")
                sender_name = parse_zelle_sender(subject, body)
                memo_text = parse_zelle_memo(body)
                conf_code = parse_zelle_confirmation(body)
                bank = parse_bank_source(from_addr, body)

                if amount is None:
                    amount = 0.0

                # Try to auto-match to a member
                member, match_type = match_member(sender_name, memo_text, amount)

                # Store in database
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                try:
                    c.execute('''INSERT INTO zelle_payments
                        (email_id, email_date, sender_name, sender_email, amount, memo,
                         confirmation_code, bank_source, raw_subject, raw_body_snippet,
                         matched_member_id, matched_member_name, matched_member_email,
                         status, auto_matched, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (eid_str, date_str, sender_name, from_addr, amount, memo_text,
                         conf_code, bank, subject, body[:500],
                         member['id'] if member else None,
                         member['full_name'] if member else None,
                         member['email'] if member else None,
                         'auto_verified' if member else 'pending',
                         1 if member else 0,
                         datetime.now().isoformat()))
                    conn.commit()

                    payment_id = c.lastrowid
                    results['new_payments'] += 1

                    if member:
                        results['auto_matched'] += 1
                        # Auto-update member balance
                        c.execute('''UPDATE members SET
                            total_paid = total_paid + ?,
                            balance_due = MAX(0, balance_due - ?),
                            updated_at = ?
                            WHERE id = ?''',
                            (amount, amount, datetime.now().isoformat(), member['id']))

                        # Add to payment history
                        receipt = f"ZP-{datetime.now().strftime('%Y%m%d')}-{payment_id:04d}"
                        c.execute('''INSERT INTO payment_history
                            (member_id, member_name, payment_type, amount, description,
                             payment_method, zelle_payment_id, status, receipt_number)
                            VALUES (?, ?, ?, ?, ?, 'Zelle', ?, 'completed', ?)''',
                            (member['id'], member['full_name'], 'Membership',
                             amount, f"Zelle from {sender_name}: {memo_text or 'No memo'}",
                             payment_id, receipt))
                        conn.commit()

                    results['payments'].append({
                        'id': payment_id,
                        'sender': sender_name,
                        'amount': amount,
                        'memo': memo_text,
                        'matched': member['full_name'] if member else None,
                        'match_type': match_type,
                        'status': 'auto_verified' if member else 'pending'
                    })

                except sqlite3.IntegrityError:
                    pass  # Duplicate
                finally:
                    conn.close()

            except Exception as e:
                results['errors'].append(f"Email {eid}: {str(e)[:100]}")

        mail.logout()

    except Exception as e:
        results['errors'].append(f"IMAP error: {str(e)[:200]}")

    # Log poll results
    duration_ms = int((time.time() - start_time) * 1000)
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO poll_log (poll_time, emails_checked, new_payments_found, auto_matched, errors, duration_ms)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (datetime.now().isoformat(), results['emails_checked'], results['new_payments'],
             results['auto_matched'], json.dumps(results['errors']), duration_ms))
        conn.commit()
        conn.close()
    except Exception:
        pass

    results['duration_ms'] = duration_ms
    return results


# ====== BACKGROUND POLLER ======

_poller_thread = None
_poller_running = False


def background_poller():
    """Background thread that polls Gmail periodically"""
    global _poller_running
    print(f"[POLLER] Background poller started (interval: {POLL_INTERVAL}s)")
    # Wait a bit before first poll to let Flask start up
    time.sleep(5)
    while _poller_running:
        try:
            result = poll_gmail_for_zelle(days_back=7)
            if result['new_payments'] > 0:
                print(f"[POLLER] Found {result['new_payments']} new Zelle payment(s), {result['auto_matched']} auto-matched")
            else:
                print(f"[POLLER] No new payments ({result['emails_checked']} emails checked)")
        except Exception as e:
            print(f"[POLLER] Error (will retry): {e}")
        time.sleep(POLL_INTERVAL)
    print("[POLLER] Background poller stopped")


def start_poller():
    """Start background polling"""
    global _poller_thread, _poller_running
    if _poller_running:
        return False
    _poller_running = True
    _poller_thread = threading.Thread(target=background_poller, daemon=True)
    _poller_thread.start()
    return True


def stop_poller():
    """Stop background polling"""
    global _poller_running
    _poller_running = False
    return True


# ====== REST API ENDPOINTS ======

@app.route('/api/zelle/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "service": "BANF Zelle Payment Automation",
        "status": "running",
        "poller_active": _poller_running,
        "poll_interval": POLL_INTERVAL,
        "database": DB_PATH,
        "gmail": GMAIL_ADDRESS,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/zelle/scan', methods=['POST'])
def manual_scan():
    """Trigger manual Gmail scan for Zelle payments"""
    days = 30
    try:
        data = request.get_json(silent=True)
        if data and 'days_back' in data:
            days = int(data['days_back'])
    except Exception:
        pass
    result = poll_gmail_for_zelle(days_back=days)
    return jsonify(result)


@app.route('/api/zelle/payments', methods=['GET'])
def get_payments():
    """Get all Zelle payments with optional filters"""
    status_filter = request.args.get('status', '')
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = "SELECT * FROM zelle_payments"
    params = []
    if status_filter:
        query += " WHERE status = ?"
        params.append(status_filter)
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    c.execute(query, params)
    payments = [dict(row) for row in c.fetchall()]

    # Get total count
    count_query = "SELECT COUNT(*) FROM zelle_payments"
    if status_filter:
        count_query += " WHERE status = ?"
        c.execute(count_query, [status_filter])
    else:
        c.execute(count_query)
    total = c.fetchone()[0]

    conn.close()
    return jsonify({"payments": payments, "total": total, "limit": limit, "offset": offset})


@app.route('/api/zelle/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    """Get single payment detail"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM zelle_payments WHERE id = ?", (payment_id,))
    payment = c.fetchone()
    conn.close()
    if payment:
        return jsonify(dict(payment))
    return jsonify({"error": "Payment not found"}), 404


@app.route('/api/zelle/payments/<int:payment_id>/verify', methods=['POST'])
def verify_payment(payment_id):
    """Manually verify/approve a pending payment"""
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}
    member_id = data.get('member_id', '')
    member_name = data.get('member_name', '')
    verified_by = data.get('verified_by', 'admin')

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Get payment
    c.execute("SELECT * FROM zelle_payments WHERE id = ?", (payment_id,))
    payment = c.fetchone()
    if not payment:
        conn.close()
        return jsonify({"error": "Payment not found"}), 404

    payment = dict(payment)

    # Update payment status
    c.execute('''UPDATE zelle_payments SET
        status = 'verified',
        matched_member_id = COALESCE(?, matched_member_id),
        matched_member_name = COALESCE(?, matched_member_name),
        verified_by = ?,
        verified_at = ?,
        updated_at = ?
        WHERE id = ?''',
        (member_id or None, member_name or None, verified_by,
         datetime.now().isoformat(), datetime.now().isoformat(), payment_id))

    # Update member balance if member specified
    mid = member_id or payment.get('matched_member_id')
    if mid:
        c.execute('''UPDATE members SET
            total_paid = total_paid + ?,
            balance_due = MAX(0, balance_due - ?),
            updated_at = ?
            WHERE id = ?''',
            (payment['amount'], payment['amount'], datetime.now().isoformat(), mid))

        # Add to payment history
        receipt = f"ZP-{datetime.now().strftime('%Y%m%d')}-{payment_id:04d}"
        c.execute('''INSERT INTO payment_history
            (member_id, member_name, payment_type, amount, description,
             payment_method, zelle_payment_id, status, receipt_number)
            VALUES (?, ?, 'Membership', ?, ?, 'Zelle', ?, 'completed', ?)''',
            (mid, member_name or payment.get('matched_member_name', ''),
             payment['amount'],
             f"Verified Zelle from {payment['sender_name']}",
             payment_id, receipt))

    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": f"Payment #{payment_id} verified"})


@app.route('/api/zelle/payments/<int:payment_id>/reject', methods=['POST'])
def reject_payment(payment_id):
    """Reject a payment (mark as not valid)"""
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}
    reason = data.get('reason', '')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''UPDATE zelle_payments SET status = 'rejected', memo = COALESCE(memo,'') || ' [REJECTED: ' || ? || ']',
        updated_at = ? WHERE id = ?''',
        (reason, datetime.now().isoformat(), payment_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": f"Payment #{payment_id} rejected"})


@app.route('/api/zelle/payments/<int:payment_id>/match', methods=['POST'])
def match_payment_to_member(payment_id):
    """Manually match a payment to a member"""
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}
    member_id = data.get('member_id')
    if not member_id:
        return jsonify({"error": "member_id required"}), 400

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM members WHERE id = ?", (member_id,))
    member = c.fetchone()
    if not member:
        conn.close()
        return jsonify({"error": "Member not found"}), 404

    member = dict(member)
    c.execute('''UPDATE zelle_payments SET
        matched_member_id = ?, matched_member_name = ?, matched_member_email = ?,
        status = 'verified', auto_matched = 0, verified_at = ?, updated_at = ?
        WHERE id = ?''',
        (member['id'], member['full_name'], member['email'],
         datetime.now().isoformat(), datetime.now().isoformat(), payment_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "member": member['full_name']})


@app.route('/api/zelle/stats', methods=['GET'])
def get_stats():
    """Get payment statistics dashboard data"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    stats = {}

    # Total payments
    c.execute("SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM zelle_payments")
    row = c.fetchone()
    stats['total_payments'] = row[0]
    stats['total_amount'] = round(row[1], 2)

    # By status
    c.execute("SELECT status, COUNT(*), COALESCE(SUM(amount), 0) FROM zelle_payments GROUP BY status")
    stats['by_status'] = {r[0]: {'count': r[1], 'amount': round(r[2], 2)} for r in c.fetchall()}

    # Auto-matched vs manual
    c.execute("SELECT auto_matched, COUNT(*) FROM zelle_payments GROUP BY auto_matched")
    stats['auto_vs_manual'] = {('auto' if r[0] else 'manual'): r[1] for r in c.fetchall()}

    # Recent payments (last 7 days)
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    c.execute("SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM zelle_payments WHERE created_at >= ?", (week_ago,))
    row = c.fetchone()
    stats['last_7_days'] = {'count': row[0], 'amount': round(row[1], 2)}

    # Pending count
    c.execute("SELECT COUNT(*) FROM zelle_payments WHERE status = 'pending'")
    stats['pending_count'] = c.fetchone()[0]

    # Members with balance due
    c.execute("SELECT COUNT(*) FROM members WHERE balance_due > 0")
    stats['members_with_balance'] = c.fetchone()[0]

    # Last poll info
    c.execute("SELECT * FROM poll_log ORDER BY id DESC LIMIT 1")
    last_poll = c.fetchone()
    if last_poll:
        stats['last_poll'] = dict(last_poll)

    stats['poller_active'] = _poller_running

    conn.close()
    return jsonify(stats)


@app.route('/api/zelle/members', methods=['GET'])
def get_members():
    """Get member list for matching dropdown"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM members ORDER BY full_name")
    members = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify({"members": members})


@app.route('/api/zelle/members/<member_id>/payments', methods=['GET'])
def get_member_payments(member_id):
    """Get payment history for a specific member"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Get member info
    c.execute("SELECT * FROM members WHERE id = ?", (member_id,))
    member = c.fetchone()
    if not member:
        conn.close()
        return jsonify({"error": "Member not found"}), 404

    # Get payment history
    c.execute('''SELECT ph.*, zp.sender_name as zelle_sender, zp.bank_source
        FROM payment_history ph
        LEFT JOIN zelle_payments zp ON ph.zelle_payment_id = zp.id
        WHERE ph.member_id = ?
        ORDER BY ph.created_at DESC''', (member_id,))
    payments = [dict(row) for row in c.fetchall()]

    conn.close()
    return jsonify({"member": dict(member), "payments": payments})


@app.route('/api/zelle/history', methods=['GET'])
def get_payment_history():
    """Get full payment history across all members"""
    limit = int(request.args.get('limit', 50))
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT ph.*, zp.sender_name as zelle_sender, zp.bank_source
        FROM payment_history ph
        LEFT JOIN zelle_payments zp ON ph.zelle_payment_id = zp.id
        ORDER BY ph.created_at DESC LIMIT ?''', (limit,))
    history = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify({"history": history, "count": len(history)})


@app.route('/api/zelle/poller/start', methods=['POST'])
def api_start_poller():
    """Start the background Gmail poller"""
    if start_poller():
        return jsonify({"success": True, "message": "Poller started", "interval": POLL_INTERVAL})
    return jsonify({"success": False, "message": "Poller already running"})


@app.route('/api/zelle/poller/stop', methods=['POST'])
def api_stop_poller():
    """Stop the background Gmail poller"""
    stop_poller()
    return jsonify({"success": True, "message": "Poller stopped"})


@app.route('/api/zelle/poller/status', methods=['GET'])
def poller_status():
    """Get poller status and recent log"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM poll_log ORDER BY id DESC LIMIT 10")
    logs = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify({
        "active": _poller_running,
        "interval_seconds": POLL_INTERVAL,
        "recent_polls": logs
    })


@app.route('/api/zelle/test/seed', methods=['POST'])
def seed_test_data():
    """Seed database with test Zelle payment data (for demo/testing)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    test_payments = [
        {
            'email_id': 'test_zelle_001',
            'email_date': 'Mon, 10 Feb 2026 09:15:00 -0500',
            'sender_name': 'Sunil Banerjee',
            'sender_email': 'sunil.banerjee@gmail.com',
            'amount': 150.00,
            'memo': 'Membership - Sunil Banerjee Family',
            'confirmation_code': 'ZEL20260210001',
            'bank_source': 'Chase',
            'raw_subject': 'You received $150.00 from Sunil Banerjee via Zelle',
            'status': 'pending',
            'auto_matched': 0,
        },
        {
            'email_id': 'test_zelle_002',
            'email_date': 'Tue, 11 Feb 2026 14:30:00 -0500',
            'sender_name': 'Priya Sen',
            'sender_email': 'priya.sen@gmail.com',
            'amount': 100.00,
            'memo': 'BANF Membership 2026',
            'confirmation_code': 'ZEL20260211002',
            'bank_source': 'Bank of America',
            'raw_subject': 'Zelle payment received: $100.00 from Priya Sen',
            'status': 'auto_verified',
            'auto_matched': 1,
            'matched_member_id': 'm_sen',
            'matched_member_name': 'Priya Sen',
        },
        {
            'email_id': 'test_zelle_003',
            'email_date': 'Wed, 12 Feb 2026 10:00:00 -0500',
            'sender_name': 'Amit Roy',
            'sender_email': 'amit.roy@gmail.com',
            'amount': 250.00,
            'memo': 'Family Membership - Roy',
            'confirmation_code': 'ZEL20260212003',
            'bank_source': 'Wells Fargo',
            'raw_subject': 'You received $250.00 from Amit Roy through Zelle',
            'status': 'auto_verified',
            'auto_matched': 1,
            'matched_member_id': 'm_roy',
            'matched_member_name': 'Amit Roy',
        },
        {
            'email_id': 'test_zelle_004',
            'email_date': 'Thu, 13 Feb 2026 11:45:00 -0500',
            'sender_name': 'Unknown Person',
            'sender_email': 'random.person@yahoo.com',
            'amount': 75.00,
            'memo': 'Saraswati Puja donation',
            'confirmation_code': 'ZEL20260213004',
            'bank_source': 'Chase',
            'raw_subject': 'Zelle: You received $75.00',
            'status': 'pending',
            'auto_matched': 0,
        },
        {
            'email_id': 'test_zelle_005',
            'email_date': 'Fri, 14 Feb 2026 08:20:00 -0500',
            'sender_name': 'Soham Ghosh',
            'sender_email': 'soham.ghosh@gmail.com',
            'amount': 375.00,
            'memo': 'Membership - Ghosh Family',
            'confirmation_code': 'ZEL20260214005',
            'bank_source': 'Chase',
            'raw_subject': 'You received $375.00 from Soham Ghosh via Zelle',
            'status': 'auto_verified',
            'auto_matched': 1,
            'matched_member_id': 'm_ghosh',
            'matched_member_name': 'Soham Ghosh',
        },
    ]

    inserted = 0
    for tp in test_payments:
        try:
            c.execute('''INSERT OR IGNORE INTO zelle_payments
                (email_id, email_date, sender_name, sender_email, amount, memo,
                 confirmation_code, bank_source, raw_subject, raw_body_snippet,
                 matched_member_id, matched_member_name, status, auto_matched, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, '', ?, ?, ?, ?, ?)''',
                (tp['email_id'], tp['email_date'], tp['sender_name'], tp['sender_email'],
                 tp['amount'], tp['memo'], tp['confirmation_code'], tp['bank_source'],
                 tp['raw_subject'],
                 tp.get('matched_member_id'), tp.get('matched_member_name'),
                 tp['status'], tp['auto_matched'], datetime.now().isoformat()))
            if c.rowcount > 0:
                inserted += 1

                # Also add to payment history for verified payments
                if tp['status'] == 'auto_verified' and tp.get('matched_member_id'):
                    pid = c.lastrowid
                    receipt = f"ZP-{datetime.now().strftime('%Y%m%d')}-{pid:04d}"
                    c.execute('''INSERT INTO payment_history
                        (member_id, member_name, payment_type, amount, description,
                         payment_method, zelle_payment_id, status, receipt_number)
                        VALUES (?, ?, 'Membership', ?, ?, 'Zelle', ?, 'completed', ?)''',
                        (tp['matched_member_id'], tp['matched_member_name'],
                         tp['amount'], f"Zelle from {tp['sender_name']}: {tp['memo']}",
                         pid, receipt))
        except Exception as e:
            print(f"[SEED] Error: {e}")

    conn.commit()
    conn.close()
    return jsonify({"success": True, "inserted": inserted, "total_test": len(test_payments)})


# ====== MAIN ======

if __name__ == '__main__':
    init_db()
    print("=" * 60)
    print("[ZELLE] BANF Zelle Payment Automation Service")
    print("=" * 60)
    print(f"  Gmail:     {GMAIL_ADDRESS}")
    print(f"  Database:  {DB_PATH}")
    print(f"  Server:    http://localhost:5002")
    print(f"  Poll Int:  {POLL_INTERVAL}s")
    print("=" * 60)
    print()
    print("  Endpoints:")
    print("    GET  /api/zelle/health          - Health check")
    print("    POST /api/zelle/scan            - Manual scan Gmail")
    print("    GET  /api/zelle/payments        - List payments")
    print("    GET  /api/zelle/payments/<id>   - Payment detail")
    print("    POST /api/zelle/payments/<id>/verify  - Verify payment")
    print("    POST /api/zelle/payments/<id>/reject  - Reject payment")
    print("    POST /api/zelle/payments/<id>/match   - Match to member")
    print("    GET  /api/zelle/stats           - Dashboard stats")
    print("    GET  /api/zelle/members         - Member list")
    print("    GET  /api/zelle/history         - Payment history")
    print("    POST /api/zelle/poller/start    - Start auto-poll")
    print("    POST /api/zelle/poller/stop     - Stop auto-poll")
    print("    GET  /api/zelle/poller/status   - Poller status")
    print("    POST /api/zelle/test/seed       - Seed test data")
    print()

    # Auto-start poller
    start_poller()

    app.run(host='0.0.0.0', port=5002, debug=False)
