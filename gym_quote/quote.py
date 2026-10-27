"""Quote calculation: subtotal, breakdown and final result (R3 to R7).

No function in this module does input or output (R8).
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from gym_quote.adjustments import (
    apply_group_discount,
    apply_premium_surcharge,
    apply_special_offer,
)
from gym_quote.catalog import EXTRAS, PLANS, has_premium_extra, is_valid_selection

INVALID = -1


@dataclass(frozen=True)
class QuoteBreakdown:
    """Every step of a valid quote, for display in the command line (R8)."""

    subtotal: Decimal
    group_discount: Decimal
    special_offer: Decimal
    premium_surcharge: Decimal
    total: int


def calculate_subtotal(plan, extras, members):
    """Return (plan price + extras price) x members (R3).

    The selection must already be valid (see catalog.is_valid_selection).
    """
    per_member = PLANS[plan] + sum((EXTRAS[extra] for extra in extras), Decimal("0"))
    return per_member * members


def round_half_up(amount):
    """Round to a whole number, halves going up (R7).

    Python's round() rounds halves to even (122.5 -> 122), so Decimal is used.
    """
    return int(Decimal(str(amount)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def build_quote(plan, extras, members):
    """Apply R3 -> R4 -> R5 -> R6 -> R7; return None if the selection is invalid."""
    extras = list(extras)
    if not is_valid_selection(plan, extras, members):
        return None
    subtotal = calculate_subtotal(plan, extras, members)
    after_group = apply_group_discount(subtotal, members)
    after_offer = apply_special_offer(after_group)
    final = apply_premium_surcharge(after_offer, has_premium_extra(extras))
    return QuoteBreakdown(
        subtotal=subtotal,
        group_discount=subtotal - after_group,
        special_offer=after_group - after_offer,
        premium_surcharge=final - after_offer,
        total=round_half_up(final),
    )


def calculate_total(plan, extras, members):
    """Return the rounded monthly total, or -1 if the selection is invalid (R7)."""
    quote = build_quote(plan, extras, members)
    return INVALID if quote is None else quote.total
