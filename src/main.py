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

def calculate_average_price(total_amount: float, item_count: int) -> float:
    """Calculates average price per item.
    BUG: Missing guard for item_count == 0 (ZeroDivisionError crash in production).
    """
    return total_amount / item_count

def process_user_checkout(user_id: str, cart_items: list) -> dict:
    """Processes user checkout.
    BUG: Calling generate_receipt_id without importing it (NameError crash).
    """
    receipt_id = generate_receipt_id(user_id)
    return {"user_id": user_id, "receipt_id": receipt_id, "items": len(cart_items)}
