import logging
import os
import smtplib
import ssl
from email.message import EmailMessage

logger = logging.getLogger()
logger.setLevel(logging.INFO)

gmail_user = os.getenv("GMAIL_USER")
gmail_password = os.getenv("GMAIL_PASSWORD")
recipient_emails = os.getenv("RECIPIENT_EMAILS").split(", ")


def send_no_power_email(tomorrow_date, split_data):
    msg = EmailMessage()
    data_list = [f"{el['where']}\n{el['when']}" for el in split_data]
    msg.set_content("\n------------------------".join(data_list))

    msg["Subject"] = f"Split bez struje - {tomorrow_date}"
    msg["From"] = gmail_user
    msg["To"] = recipient_emails

    context = ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
        smtp.starttls(context=context)
        smtp.login(gmail_user, gmail_password)
        smtp.send_message(msg)
        logger.info("email_sent")
