"""Data model shared by the pricing functions and the command line."""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

INVALID_RESULT = -1


@dataclass(frozen=True)
class QuoteBreakdown:
    """Every step of a quote, so the command line can show each amount (R8)."""

    subtotal: float = 0.0
    group_discount: float = 0.0
    special_offer: float = 0.0
    premium_surcharge: float = 0.0
    total: int = INVALID_RESULT

    @property
    def is_valid(self) -> bool:
        """Return True when the quote has a total (R7: invalid selections give -1)."""
        return self.total != INVALID_RESULT
    
    @staticmethod
    def calculate_subtotal(plan, extras, members):
        """Return (plan price + extras price) x members (R3).

        The selection must already be valid (see catalog.is_valid_selection).
        """
        per_member = PLANS[plan] + sum((EXTRAS[extra] for extra in extras), Decimal("0"))   
        return per_member * members

    @staticmethod
    def round_half_up(amount):
        """Round to a whole number, halves going up (R7).

        Python's round() rounds halves to even (122.5 -> 122), so Decimal is used.
        """
        return int(Decimal(str(amount)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))