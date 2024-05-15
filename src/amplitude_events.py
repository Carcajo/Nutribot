from threading import Thread

from amplitude import Amplitude, BaseEvent
from config import SETTINGS

amplitude = Amplitude(SETTINGS.AMPLITUDE_API_KEY)


def user_start(user_id: int):
    Thread(target = lambda:
    amplitude.track(
        BaseEvent(
            event_type="User /start command",
            user_id=str(user_id),
        )
    )
           ).run()

def user_text_message(user_id: int, text_message):
    Thread(target = lambda:
    amplitude.track(
        BaseEvent(
            event_type="User text message",
            user_id=str(user_id),
            event_properties={
                "text": text_message,
            }
        )
    )
           ).run()

def user_voice_message(user_id: int, transcribed_text):
    Thread(target = lambda:
    amplitude.track(
        BaseEvent(
            event_type="User voice message",
            user_id=str(user_id),
            event_properties={
                "text": transcribed_text,
            }
        )
    )
    ).run()

def user_photo_message(user_id: int):
    Thread(target = lambda:
    amplitude.track(
        BaseEvent(
            event_type="User sends a photo",
            user_id=str(user_id),
        )
    )
).run()
