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

def drop_empty(config: dict) -> dict:
    """Removes empty-valued keys in place.
    BUG: RuntimeError â€” mutating a dict (del) while iterating it.
    """
    for key in config:
        if not config[key]:
            del config[key]
    return config
