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

def order_total(prices: dict) -> float:
    """Sums the 'price' field of every line item.
    BUG: direct ["price"] access â€” KeyError when a line item omits it.
    """
    return sum(item["price"] for item in prices.values())
