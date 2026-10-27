"""Data model shared by the pricing functions and the command line."""
from dataclasses import dataclass

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
