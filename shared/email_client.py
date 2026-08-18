"""IMAP/SMTP client for zsazsa@zafconsultancy.org.

Stdlib only (imaplib/smtplib), mirroring the readonly-IMAP pattern already
proven in VV Outreach's mail_check.py — never disturbs the mailbox's own
\\Seen flags when just checking for new mail.

Reads all connection details from env vars (see .env.example). Credentials
live only as the EMAIL_PASSWORD GitHub Actions repo secret, never in a file.
"""

import email
import imaplib
import os
import smtplib
from email.message import EmailMessage


def _config():
    return {
        "address": os.environ["EMAIL_ADDRESS"],
        "password": os.environ["EMAIL_PASSWORD"],
        "imap_host": os.environ.get("EMAIL_IMAP_HOST", "mail.zafconsultancy.org"),
        "imap_port": int(os.environ.get("EMAIL_IMAP_PORT", 993)),
        "smtp_host": os.environ.get("EMAIL_SMTP_HOST", "mail.zafconsultancy.org"),
        "smtp_port": int(os.environ.get("EMAIL_SMTP_PORT", 465)),
    }


def send_email(to, subject, body):
    cfg = _config()
    msg = EmailMessage()
    msg["From"] = cfg["address"]
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL(cfg["smtp_host"], cfg["smtp_port"]) as server:
        server.login(cfg["address"], cfg["password"])
        server.send_message(msg)


def check_unread(limit=10):
    """Readonly — does not mark messages as read."""
    cfg = _config()
    results = []
    with imaplib.IMAP4_SSL(cfg["imap_host"], cfg["imap_port"]) as server:
        server.login(cfg["address"], cfg["password"])
        server.select("INBOX", readonly=True)
        status, data = server.search(None, "UNSEEN")
        if status != "OK":
            return results
        ids = data[0].split()[-limit:]
        for msg_id in ids:
            status, msg_data = server.fetch(msg_id, "(BODY.PEEK[HEADER])")
            if status != "OK":
                continue
            headers = email.message_from_bytes(msg_data[0][1])
            results.append(
                {
                    "from": headers.get("From"),
                    "subject": headers.get("Subject"),
                    "date": headers.get("Date"),
                }
            )
    return results


def test_connection():
    """Login-only check for both IMAP and SMTP — sends/reads nothing."""
    cfg = _config()
    with imaplib.IMAP4_SSL(cfg["imap_host"], cfg["imap_port"]) as server:
        server.login(cfg["address"], cfg["password"])
        server.select("INBOX", readonly=True)
    with smtplib.SMTP_SSL(cfg["smtp_host"], cfg["smtp_port"]) as server:
        server.login(cfg["address"], cfg["password"])
    return True
