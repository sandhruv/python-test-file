# Events API contract

`POST https://events.example.com/v1/events`

| Field | Type | Notes |
|---|---|---|
| `type` | string | Event name, non-empty |
| `user_id` | integer | Positive user id |
| `properties` | object | Optional event metadata |
| `timestamp` | integer | **Epoch milliseconds, UTC** (13 digits) |

The API rejects events whose `timestamp` is more than 5 minutes old or in the future.
