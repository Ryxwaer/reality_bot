# app/emailer.py
import smtplib
from email.mime.text import MIMEText
from typing import List, Dict

def send_email(subject: str, body: str, to: str, from_email: str, smtp_server: str, smtp_port: int, smtp_user: str, smtp_password: str):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, [to], msg.as_string())

def notify_new_listings(new_listings: List[Dict], to_email: str, from_email: str, smtp_server: str, smtp_port: int, smtp_user: str, smtp_password: str):
    if not new_listings:
        return

    subject = "New Real Estate Listings"
    body = "\n\n".join([str(listing) for listing in new_listings])
    send_email(subject, body, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password)
