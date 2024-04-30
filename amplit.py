from config import Settings
from threading import Thread
import requests
import time
import logging


settings = Settings()
logger = logging.getLogger(__name__)


class Amplitude:
    def __init__(self, api_key, user_id=None):
        self.api_key = api_key
        self.user_id = user_id
        self.base_url = "https://api.amplitude.com"
        self.session = requests.Session()

    def set_user_id(self, user_id):
        self.user_id = user_id

    def track(self, event_type, event_properties=None, user_id=None):
        user_id = user_id or self.user_id
        if not user_id:
            logger.warning("No user ID provided, skipping event tracking.")
            return

        payload = {
            "api_key": self.api_key,
            "event": {
                "user_id": str(user_id),
                "event_type": event_type,
                "event_properties": event_properties or {},
                "time": int(time.time()),
            },
        }

        response = self.session.post(f"{self.base_url}/2/httpapi", json=payload)
        response.raise_for_status()
        logger.info(f"Event '{event_type}' tracked for user '{user_id}'")

    def __del__(self):
        self.session.close()


client = Amplitude(settings.AMPLITUDE_API_KEY)


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
