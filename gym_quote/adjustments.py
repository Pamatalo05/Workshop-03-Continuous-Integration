"""Discounts and surcharges (R4, R5, R6).

Every function receives an amount (Decimal) and returns an amount,
so they can be developed and tested without the rest of the quote.
"""

from decimal import Decimal

GROUP_MIN_MEMBERS = 2
GROUP_DISCOUNT_RATE = Decimal("0.10")

HIGH_OFFER_THRESHOLD = Decimal("400")
HIGH_OFFER_AMOUNT = Decimal("50")
LOW_OFFER_THRESHOLD = Decimal("200")
LOW_OFFER_AMOUNT = Decimal("20")

PREMIUM_SURCHARGE_RATE = Decimal("0.15")


def apply_group_discount(amount, members):
    """Apply 10% off when there are 2 or more members (R4)."""
    if members >= GROUP_MIN_MEMBERS:
        return amount * (1 - GROUP_DISCOUNT_RATE)
    return amount


def apply_special_offer(amount):
    """Subtract 50 if amount > 400, else 20 if amount > 200 (R5).

    Applied to the amount after R4. The two offers never add up.
    """
    if amount > HIGH_OFFER_THRESHOLD:
        return amount - HIGH_OFFER_AMOUNT
    if amount > LOW_OFFER_THRESHOLD:
        return amount - LOW_OFFER_AMOUNT
    return amount


def apply_premium_surcharge(amount, has_premium):
    """Add 15% to the amount after R5 when there is a premium extra (R6)."""
    if has_premium:
        return amount * (1 + PREMIUM_SURCHARGE_RATE)
    return amount
