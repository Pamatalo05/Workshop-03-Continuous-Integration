"""Tests for the quote breakdown and the final result (R4 to R7)."""

from decimal import Decimal

from gym_quote.quote import INVALID, build_quote, calculate_total


def test_breakdown_shows_each_step():
    """PREMIUM + GROUP_CLASSES + SPA x 2: 230, -23, -20, +28.05, total 215."""
    quote = build_quote("PREMIUM", ["GROUP_CLASSES", "SPA"], 2)
    assert quote.subtotal == Decimal("230")
    assert quote.group_discount == Decimal("23")
    assert quote.special_offer == Decimal("20")
    assert quote.premium_surcharge == Decimal("28.05")
    assert quote.total == 215


def test_breakdown_without_discounts():
    """One member under 200 gets no discount, offer or surcharge."""
    quote = build_quote("BASIC", [], 1)
    assert quote.group_discount == quote.special_offer == quote.premium_surcharge == 0
    assert quote.total == 30


def test_invalid_selection_has_no_breakdown():
    """An invalid selection gives no breakdown."""
    assert build_quote("BASIC", ["SPA"], 1) is None


def test_r7_total_is_rounded_half_up():
    """R7: 121.5 is rounded to 122 only at the end (BASIC + GROUP_CLASSES x 3)."""
    assert calculate_total("BASIC", ["GROUP_CLASSES"], 3) == 122


def test_r7_invalid_selection_returns_minus_one():
    """R7: an invalid selection gives -1."""
    assert calculate_total("GOLD", [], 1) == INVALID


def test_r5_uses_the_amount_after_the_group_discount():
    """R5 is applied after R4: 210 - 21 = 189 is not above 200, so no offer."""
    quote = build_quote("PREMIUM", [], 3)
    assert quote.subtotal == Decimal("210")
    assert quote.group_discount == Decimal("21")
    assert quote.special_offer == 0
    assert quote.total == 189


def test_r6_uses_the_amount_after_the_special_offer():
    """R6 is applied after R5: (420 - 42 - 20) x 1.15 = 411.7, rounded to 412."""
    quote = build_quote("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM"], 3)
    assert quote.special_offer == Decimal("20")
    assert quote.premium_surcharge == Decimal("53.70")
    assert quote.total == 412


def test_r4_r5_r6_together_with_the_high_offer():
    """R4, R5 (-50 above 400) and R6 together: (620 - 62 - 50) x 1.15 = 584.2 -> 584."""
    quote = build_quote("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM", "GROUP_CLASSES"], 4)
    assert quote.subtotal == Decimal("620")
    assert quote.group_discount == Decimal("62")
    assert quote.special_offer == Decimal("50")
    assert quote.premium_surcharge == Decimal("76.2")
    assert quote.total == 584
