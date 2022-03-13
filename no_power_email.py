import os
import smtplib
import ssl
from email.message import EmailMessage

gmail_user = os.getenv("GMAIL_USER")
gmail_password = os.getenv("GMAIL_PASSWORD")


def send_no_power_email(split_data):
    msg = EmailMessage()
    msg.set_content(f"{split_data['where']}\n\n{split_data['when']}")

    msg["Subject"] = "Split bez struje"
    msg["From"] = "lukabotmail@gmail.com"
    msg["To"] = ["kilic.luka@gmail.com", "marijakardum1@gmail.com"]

    context = ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
        smtp.starttls(context=context)
        smtp.login(gmail_user, gmail_password)
        smtp.send_message(msg)
