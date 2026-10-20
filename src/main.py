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

class BatchImporter:
    """Accumulates imported rows.
    BUG: mutable class attribute â€” `rows` is shared across ALL instances;
    every importer sees every other importer's rows.
    """
    rows = []

    def add(self, row: dict):
        self.rows.append(row)
        return self
