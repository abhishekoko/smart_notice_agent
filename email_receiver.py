import os
import imaplib
import email
import json
import time
from datetime import datetime

# ==============================
# CONFIGURATION (Edit here)
# ==============================
IMAP_HOST = "imap.gmail.com"  # Always use Gmail IMAP host
IMAP_PORT = 993
IMAP_USER = "abhishek73197319@gmail.com"  # Replace with your Gmail address
IMAP_PASSWORD = "pqhw ozvy uxwd thme"  # Use Gmail App Password, not your login password
POLL_INTERVAL = 60  # seconds between checks

SAVE_DIR = "received_emails"
os.makedirs(SAVE_DIR, exist_ok=True)


# ==============================
# Email Receiver Class
# ==============================
class EmailReceiver:
    def __init__(self):
        self.host = IMAP_HOST
        self.port = IMAP_PORT
        self.username = IMAP_USER
        self.password = IMAP_PASSWORD
        self.poll = POLL_INTERVAL

    def connect_imap(self):
        """Connect to IMAP inbox."""
        try:
            mail = imaplib.IMAP4_SSL(self.host, self.port)
            mail.login(self.username, self.password)
            print("Connected to Gmail IMAP successfully.")
            return mail
        except imaplib.IMAP4.error as e:
            print(f"IMAP login failed: {e}")
            return None

    def fetch_unseen_emails(self):
        """Fetch unseen emails and save locally."""
        mail = self.connect_imap()
        if not mail:
            return

        mail.select("inbox")
        result, data = mail.search(None, "UNSEEN")
        if result != "OK":
            print("Could not search inbox.")
            return

        for num in data[0].split():
            result, msg_data = mail.fetch(num, "(RFC822)")
            if result != "OK":
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            subject = msg.get("subject", "(no subject)")
            sender = msg.get("from", "(unknown sender)")
            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            body += payload.decode(errors="ignore")
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors="ignore")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{SAVE_DIR}/email_{timestamp}.json"

            with open(filename, "w", encoding="utf-8") as f:
                json.dump({
                    "from": sender,
                    "subject": subject,
                    "body": body.strip()
                }, f, ensure_ascii=False, indent=2)

            print(f"Saved new email: '{subject}' -> {filename}")

        mail.logout()

    def run(self):
        """Main loop — check inbox periodically."""
        print("Email receiver started... Press Ctrl+C to stop.")
        try:
            while True:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for new emails...")
                self.fetch_unseen_emails()
                time.sleep(self.poll)
        except KeyboardInterrupt:
            print("Stopped by user.")


# ==============================
# Run Script
# ==============================
if __name__ == "__main__":
    receiver = EmailReceiver()
    receiver.run()
