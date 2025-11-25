from twilio.rest import Client
from app.core.config import settings

client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)

def send_whatsapp_message(phone, message, media_url=None):
    data = {
        "from_": settings.TWILIO_WHATSAPP_FROM,
        "to": f"whatsapp:{phone}",
        "body": message
    }
    if media_url:
        data["media_url"] = [media_url]

    client.messages.create(**data)
