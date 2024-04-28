import amplitude
from threading import Thread
from config import settings

client = amplitude.Client(settings.AMPLITUDE_API_KEY)

def send_event(event_type, user_id, event_properties=None):
    event_data = {
        "event_type": event_type,
        "user_id": str(user_id),
        "event_properties": event_properties or {},
    }

    def send_event_async():
        client.track(**event_data)

    thread = Thread(target=send_event_async)
    thread.start()