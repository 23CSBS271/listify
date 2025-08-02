import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_whatsapp(to_number, message):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("+14155238886")

    if not all([account_sid, auth_token, from_number]):
        print("Twilio credentials missing.")
        return False

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_=from_number,
            body=message,
            to=f"whatsapp:{to_number}"
        )
        print("WhatsApp message SID:", message.sid)
        return True
    except Exception as e:
        print("Failed to send WhatsApp message:", e)
        return False
