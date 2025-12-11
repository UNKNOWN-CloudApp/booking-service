import os
import json
from datetime import datetime

from google.cloud import pubsub_v1
from google.auth.exceptions import DefaultCredentialsError

# Project and topic configuration
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "fluid-outcome-478808-p2")
TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "trigger")

# Lazy-initialized globals
_publisher = None
_topic_path = None


def _get_publisher():
    """
    Lazily initialize the Pub/Sub publisher.

    - On local machine without credentials:
        * print a warning
        * return (None, None) so we silently skip publishing
    - On GCP VM (with metadata credentials):
        * initialize successfully and return real publisher + topic path
    """
    global _publisher, _topic_path

    # If already initialized, reuse
    if _publisher is not None and _topic_path is not None:
        return _publisher, _topic_path

    try:
        client = pubsub_v1.PublisherClient()
        path = client.topic_path(PROJECT_ID, TOPIC_ID)
        _publisher = client
        _topic_path = path
        print(f"✅ Pub/Sub publisher initialized for topic: {path}")
        return _publisher, _topic_path
    except DefaultCredentialsError as e:
        # This is what happens on your Mac right now
        print(f"⚠️ Pub/Sub disabled (no credentials available): {e}")
        return None, None
    except Exception as e:
        # Any other unexpected error — don't crash the app
        print(f"⚠️ Failed to initialize Pub/Sub publisher: {e}")
        return None, None


def publish_new_record_trigger(record_id: str, client_name: str):
    """
    Publish a Pub/Sub message when a new booking is created.

    On local dev without credentials:
        -> this will just log a warning and return.
    On VM with credentials:
        -> this will actually send the message to Pub/Sub.
    """

    publisher, topic_path = _get_publisher()
    if publisher is None or topic_path is None:
        # No Pub/Sub available (likely local dev) -> skip sending
        return

    message_data = {
        "event_type": "NEW_BOOKING_RECORD",
        "record_id": record_id,
        "client_name": client_name,
        "timestamp": datetime.now().isoformat(),
    }

    data_bytes = json.dumps(message_data).encode("utf-8")

    attributes = {
        "source": "booking-service",
        "action": "new_booking",
    }

    try:
        future = publisher.publish(
            topic_path,
            data=data_bytes,
            **attributes,
        )
        message_id = future.result()
        print(f"✅ Published message ID: {message_id} to {topic_path}")
    except Exception as e:
        # Don't crash your booking API because Pub/Sub failed
        print(f"❌ Failed to publish Pub/Sub message: {e}")
