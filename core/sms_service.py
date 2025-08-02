import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_whatsapp(to_number, message):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")  # Should be "whatsapp:+14155238886"

    if not all([account_sid, auth_token, from_number]):
        print("Twilio credentials missing.")
        return False

    try:
        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            from_=from_number,
            to=f"whatsapp:{to_number}",
            body=message
        )
        print("WhatsApp message sent:", msg.sid)
        return True
    except Exception as e:
        print("Error sending WhatsApp:", e)
        return False
