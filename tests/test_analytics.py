from datetime import datetime, timezone

import pytest

from src.analytics import event_payload


def test_event_payload_contains_required_fields():
    payload = event_payload(
        "signup_completed",
        42,
        {"plan": "pro"},
        datetime(2026, 1, 15, 12, 0, tzinfo=timezone.utc),
    )
    assert payload["type"] == "signup_completed"
    assert payload["user_id"] == 42
    assert payload["properties"] == {"plan": "pro"}
    assert isinstance(payload["timestamp"], int)


def test_event_payload_defaults_properties_and_timestamp():
    payload = event_payload("page_viewed", 7)
    assert payload["properties"] == {}
    assert isinstance(payload["timestamp"], int)


def test_event_payload_rejects_empty_type():
    with pytest.raises(ValueError):
        event_payload("  ", 1)


def test_event_payload_rejects_invalid_user():
    with pytest.raises(ValueError):
        event_payload("page_viewed", 0)
