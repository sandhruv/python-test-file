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

def make_multipliers():
    """Builds a list of multiplier functions.
    BUG: late binding â€” all closures share the final value of i (all return *10).
    """
    return [lambda x: x * i for i in range(1, 5)]
