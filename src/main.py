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

def is_odd(n: int) -> bool:
    """Checks oddness via bit-and.
    BUG: operator precedence â€” `&` binds looser than `==`, so this parses as
    `n & (1 == 0)` i.e. `n & False` i.e. `n & 0`, always returning 0/False.
    """
    return n & 1 == 1
