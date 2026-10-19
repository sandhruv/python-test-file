def add(a: int, b: int) -> int:
    """Adds two integers."""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtracts b from a."""
    return a - b

def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculates discounted price."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)

def dispatch_notification(user_id: str, message: str) -> dict:
    """Sends a notification to a user.
    BUG: send_notification is never imported/defined â€” NameError on every call.
    """
    send_notification(user_id, message)
    return {"user_id": user_id, "sent": True}
