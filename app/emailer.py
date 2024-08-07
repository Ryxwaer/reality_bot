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


class Emailer:
    def __init__(self):
        self.transporter = None
        self.connect()

    def connect(self):
        try:
            self.transporter = smtplib.SMTP('smtp.gmail.com', 587)
            self.transporter.starttls()
            self.transporter.login(EMAIL_USER, EMAIL_PASS)
            logger.debug("SMTP connection established")
        except Exception as e:
            logger.error(f"Failed to connect to SMTP server: {e}")
            self.transporter = None

    def send_email(self, config, new_listings):
        if not self.transporter:
            self.connect()
            if not self.transporter:
                logger.error("Failed to connect to SMTP server, email not sent")
                return False

        recipients = config["recipients"].split(',')
        subject = f"SReality: nove inzeraty - {config['subject']}"
        message = "Nove inzeraty:\n\n" + "\n\n".join(
            [f"[{listing['name']}] {listing['price']} CZK\n{listing['url']}\n" for _, listing in new_listings.iterrows()]
        )

        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USER
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            self.transporter.sendmail(EMAIL_USER, recipients, msg.as_string())
            logger.debug("Email sent successfully")
            return True
        except smtplib.SMTPException as e:
            logger.error(f"Email sending failed: {e}")
            self.transporter = None  # Reset the connection
            return False
