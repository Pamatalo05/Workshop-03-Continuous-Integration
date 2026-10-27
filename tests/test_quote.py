"""Tests for the QuoteBreakdown data model."""
from gym_quote.quote import INVALID_RESULT, QuoteBreakdown


def test_default_breakdown_is_invalid():
    """An empty breakdown carries the -1 result of R7."""
    breakdown = QuoteBreakdown()
    assert breakdown.total == INVALID_RESULT
    assert not breakdown.is_valid


def test_breakdown_with_total_is_valid():
    """A breakdown with a total is a valid quote."""
    assert QuoteBreakdown(subtotal=30.0, total=30).is_valid
