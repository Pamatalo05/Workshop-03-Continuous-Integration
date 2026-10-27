"""Tests for the discounts and the surcharge (R4, R5, R6)."""

from decimal import Decimal

import pytest

from gym_quote.adjustments import (
    apply_group_discount,
    apply_premium_surcharge,
    apply_special_offer,
)


def test_r4_one_member_has_no_group_discount():
    """R4: one member pays the full subtotal."""
    assert apply_group_discount(Decimal("100"), 1) == Decimal("100")


@pytest.mark.parametrize("members", [2, 5])
def test_r4_two_or_more_members_get_ten_percent(members):
    """R4: 2 or more members get 10% off."""
    assert apply_group_discount(Decimal("100"), members) == Decimal("90")


@pytest.mark.parametrize(
    "amount, expected",
    [
        (Decimal("401"), Decimal("351")),
        (Decimal("400"), Decimal("380")),
        (Decimal("201"), Decimal("181")),
        (Decimal("200"), Decimal("200")),
        (Decimal("150"), Decimal("150")),
    ],
)
def test_r5_special_offer_limits(amount, expected):
    """R5: -50 above 400, else -20 above 200; the limits are strict and never add up."""
    assert apply_special_offer(amount) == expected


def test_r6_premium_extra_adds_fifteen_percent():
    """R6: +15% with at least one premium extra."""
    assert apply_premium_surcharge(Decimal("100"), True) == Decimal("115")


def test_r6_no_premium_extra_no_surcharge():
    """R6: no surcharge without premium extras."""
    assert apply_premium_surcharge(Decimal("100"), False) == Decimal("100")
