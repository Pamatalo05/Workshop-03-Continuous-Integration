"""Tests for the subtotal and the final rounding (R3, R7)."""

from decimal import Decimal

import pytest

from gym_quote.quote import calculate_subtotal, round_half_up


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


@pytest.mark.parametrize(
    "plan, extras, members, expected",
    [
        ("BASIC", ["GROUP_CLASSES"], 2, Decimal("90")),
        ("STANDARD", ["PERSONAL_TRAINING"], 1, Decimal("70")),
        ("PREMIUM", ["GROUP_CLASSES", "SPA"], 2, Decimal("230")),
        ("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM"], 3, Decimal("420")),
    ],
)
def test_r3_subtotal_of_workshop_rows(plan, extras, members, expected):
    """R3: subtotal of several rows of the workshop table, before any discount."""
    assert calculate_subtotal(plan, extras, members) == expected


def test_r3_subtotal_does_not_depend_on_extras_order():
    """R3: the order in which the extras are chosen does not change the subtotal."""
    first = calculate_subtotal("PREMIUM", ["SPA", "GROUP_CLASSES"], 2)
    second = calculate_subtotal("PREMIUM", ["GROUP_CLASSES", "SPA"], 2)
    assert first == second


@pytest.mark.parametrize("amount, expected", [(0.5, 1), (122.5, 123), (626.0, 626)])
def test_r7_rounds_float_amounts_half_up(amount, expected):
    """R7: float amounts are rounded half up too (122.5 -> 123, unlike round())."""
    assert round_half_up(amount) == expected
