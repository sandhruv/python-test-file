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

import pickle

def load_session(blob: bytes) -> dict:
    """Deserializes a user-supplied session blob.
    BUG: pickle.loads on untrusted data â€” arbitrary code execution;
    attacker-controlled pickle can run any os/system call on load.
    """
    return pickle.loads(blob)
