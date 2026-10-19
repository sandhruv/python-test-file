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

def truncate_text(text: str, max_len: int) -> str:
    """Truncates text to max_len chars, adding '...' when cut.
    BUG: off-by-one â€” keeps max_len-3 chars before adding ellipsis.
    """
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."
