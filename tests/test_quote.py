"""Tests for the QuoteBreakdown data model."""
from decimal import Decimal
import pytest

from gym_quote.quote import (
    INVALID_RESULT, 
    QuoteBreakdown, 
    calculate_subtotal, 
    round_half_up
)


def test_default_breakdown_is_invalid():
    """An empty breakdown carries the -1 result of R7."""
    breakdown = QuoteBreakdown()
    assert breakdown.total == INVALID_RESULT
    assert not breakdown.is_valid


def test_breakdown_with_total_is_valid():
    """A breakdown with a total is a valid quote."""
    assert QuoteBreakdown(subtotal=30.0, total=30).is_valid


def test_r3_subtotal_one_member_no_extras():
    """R3: the plan price alone for one member."""
    assert calculate_subtotal("BASIC", [], 1) == Decimal("30")


def test_r3_subtotal_multiplies_by_members():
    """R3: (plan + extras) x members."""
    assert calculate_subtotal("STANDARD", ["GROUP_CLASSES"], 3) == Decimal("180")


def test_r3_subtotal_adds_every_extra():
    """R3: every extra is added once per member."""
    extras = ["SPA", "SPECIALIZED_PROGRAM", "PERSONAL_TRAINING"]
    assert calculate_subtotal("PREMIUM", extras, 4) == Decimal("660")


@pytest.mark.parametrize(
    "amount, expected",
    [
        (Decimal("121.5"), 122),
        (Decimal("122.5"), 123),
        (Decimal("215.05"), 215),
        (Decimal("411.7"), 412),
        (Decimal("30"), 30),
    ],
)
def test_r7_rounds_half_up(amount, expected):
    """R7: halves go up (122.5 -> 123, unlike round()), the rest to the nearest."""
    assert round_half_up(amount) == expected