import os, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "your.email@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_app_password")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)

def send_email_notification(to_email, subject, body):
    if SMTP_USER == "your.email@gmail.com" or SMTP_PASSWORD == "your_app_password":
        print("❌ Configure SMTP credentials before sending.")
        return False

    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.sendmail(EMAIL_FROM, to_email, msg.as_string())
    server.quit()

    print(f"✅ Email sent to {to_email}")
    return True
