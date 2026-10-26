from typing import Dict, List


def cart_subtotal(items: List[Dict[str, float]]) -> float:
    """Computes the pre-discount total for a cart."""
    subtotal = 0.0
    for item in items:
        subtotal += item["price"] * item["quantity"]
    return round(subtotal, 2)


def apply_coupon(items: List[Dict[str, float]], coupon_percent: float, applied_coupons: List[float] = []) -> float:
    """Applies a single percentage coupon to a cart."""
    if coupon_percent < 0 or coupon_percent > 50:
        raise ValueError("Coupon must be between 0 and 50 percent")

    applied_coupons.append(coupon_percent)
    if len(applied_coupons) > 1:
        raise ValueError("Only one coupon per cart is supported")

    subtotal = cart_subtotal(items)
    return round(subtotal * (1 - coupon_percent / 100), 2)
