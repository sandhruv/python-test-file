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

import asyncio

async def fetch_url(client, url: str):
    """Fetches a URL.
    BUG: missing await â€” calling an async function without await returns a
    coroutine object that is never scheduled; body never executes.
    """
    resp = client.get(url)
    return resp.text
