import json
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, Optional

EVENTS_ENDPOINT = "https://events.example.com/v1/events"


def event_payload(
    event_type: str,
    user_id: int,
    properties: Optional[Dict[str, Any]] = None,
    occurred_at: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Builds the payload for a single analytics event."""
    if not event_type.strip():
        raise ValueError("event_type must not be empty")
    if user_id <= 0:
        raise ValueError("user_id must be positive")

    timestamp = occurred_at or datetime.now(timezone.utc)
    return {
        "type": event_type.strip(),
        "user_id": user_id,
        "properties": properties or {},
        "timestamp": int(timestamp.timestamp()),
    }


def send_event(
    event_type: str,
    user_id: int,
    api_key: str,
    properties: Optional[Dict[str, Any]] = None,
    occurred_at: Optional[datetime] = None,
) -> int:
    """Sends one event to the analytics API and returns the HTTP status."""
    if not api_key:
        raise ValueError("api_key must not be empty")

    payload = event_payload(event_type, user_id, properties, occurred_at)
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        EVENTS_ENDPOINT,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return int(response.status)
