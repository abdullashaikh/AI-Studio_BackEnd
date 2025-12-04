import smtplib
from email.mime.text import MIMEText
import os

def send_email_otp(receiver_email, otp):
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("EMAIL_APP_PASSWORD")
    print(f"Sending OTP to {receiver_email}: {otp}")
    print(f"our OTP to {sender_email}: {app_password}")
    message = MIMEText(f"Your OTP is: {otp}")
    message["Subject"] = "Your OTP Code"
    message["From"] = sender_email
    message["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
