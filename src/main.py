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

def print_all(items: list) -> None:
    """Prints every element.
    BUG: off-by-one â€” range goes to len(items), last index access raises IndexError.
    """
    for i in range(len(items) + 1):
        print(items[i])
