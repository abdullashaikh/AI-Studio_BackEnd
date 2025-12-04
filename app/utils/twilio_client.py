from twilio.rest import Client
import os

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_sms_otp(phone: str, otp: str):
    message = client.messages.create(
        body=f"Your verification code is: {otp}",
        from_=TWILIO_PHONE,
        to=phone
    )
    return message.sid
