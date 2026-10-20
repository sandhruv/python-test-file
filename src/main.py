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

import copy

def clone_matrix(matrix: list) -> list:
    """Returns a copy of a 2-D matrix.
    BUG: shallow copy â€” inner lists are shared; mutating the clone mutates the original.
    """
    return copy.copy(matrix)
