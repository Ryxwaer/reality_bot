from aiosmtplib import send
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = 'your.smtp.server'
SMTP_PORT = 587
SMTP_USER = 'your_email@example.com'
SMTP_PASS = 'your_password'


async def send_email(subject, body, to_email):
    message = MIMEMultipart()
    message["From"] = SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    await send(message, hostname=SMTP_HOST, port=SMTP_PORT, username=SMTP_USER, password=SMTP_PASS, use_tls=True)
