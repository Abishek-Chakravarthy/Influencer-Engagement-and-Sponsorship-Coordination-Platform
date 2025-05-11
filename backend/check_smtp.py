import smtplib
import os

def test_smtp():
    try:
        smtp_user = os.getenv("MAILGUN_SMTP_USER")
        smtp_pass = os.getenv("MAILGUN_SMTP_PASSWORD")

        server = smtplib.SMTP('smtp.mailgun.org', 587)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.quit()
        print("SMTP connection successful!")
    except Exception as e:
        print(f"SMTP connection failed: {e}")

test_smtp()
