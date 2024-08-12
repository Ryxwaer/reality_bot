import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def compose_email_body(new_listings):
    formatted_listings = "".join(
        [f"<a href='{listing['url']}' style='text-decoration: none; color: inherit;' target='_blank'>"
         f"<div style='margin-bottom: 20px; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; box-shadow: "
         f"0 2px 8px rgba(0,0,0,0.1); transition: box-shadow 0.3s ease-in-out;'>"
         f"<h2 style='margin: 0 0 10px; font-size: 1.5em; color: #2c3e50;'>{listing['name']}</h2>"
         f"<p style='margin: 10px 0; color: #27ae60; font-weight: bold; font-size: 1.2em;'>{listing['price']} CZK</p>"
         f"<p style='margin: 5px 0; font-size: 1em; color: #555;'><strong>Locality:</strong> {listing['locality']}</p>"
         f"<p style='margin: 5px 0; font-size: 1em; color: #555;'><strong>Features:</strong> {listing['features']}</p>"
         f"</div>"
         f"</a>"
         for _, listing in new_listings.iterrows()]
    )
    return f"<html><body style='font-family: Arial, sans-serif; line-height: 1.6;'>{formatted_listings}</body></html>"


class Emailer:
    def __init__(self):
        self.transporter = None

    def connect(self):
        try:
            self.transporter = smtplib.SMTP('smtp.gmail.com', 587)
            self.transporter.starttls()
            self.transporter.login(EMAIL_USER, EMAIL_PASS)
            logger.debug("SMTP connection established")
        except Exception as e:
            logger.error(f"Failed to connect to SMTP server: {e}")
            self.transporter = None

    def disconnect(self):
        if self.transporter:
            try:
                self.transporter.quit()
                logger.debug("SMTP connection closed")
            except Exception as e:
                logger.error(f"Failed to close SMTP connection: {e}")
            self.transporter = None

    def send_email(self, config, new_listings):
        if not self.transporter:
            self.connect()
            if not self.transporter:
                logger.error("Failed to connect to SMTP server, email not sent")
                return False

        recipients = config["recipients"].split(',')
        recipients = [r.strip() for r in recipients]
        subject = f"SReality: nove inzeraty - {config['subject']}"
        message = compose_email_body(new_listings)

        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USER
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'html'))

            self.transporter.sendmail(EMAIL_USER, recipients, msg.as_string())
            logger.debug("Email sent successfully")
            return True

        except smtplib.SMTPException as e:
            logger.error(f"Email sending failed: {e}")
            self.transporter = None  # Reset the connection
            return False
