"""Tests for the catalog and the selection validation (R1, R2, R3)."""

from decimal import Decimal

import pytest

from gym_quote.catalog import (
    EXTRAS,
    PLANS,
    PREMIUM_EXTRAS,
    has_premium_extra,
    is_valid_extras,
    is_valid_members,
    is_valid_plan,
    is_valid_selection,
)


def test_r1_plan_prices():
    """R1: the plans have the monthly prices per member of the table."""
    assert PLANS == {
        "BASIC": Decimal("30"),
        "STANDARD": Decimal("45"),
        "PREMIUM": Decimal("70"),
    }


@pytest.mark.parametrize("plan", ["BASIC", "STANDARD", "PREMIUM"])
def test_r1_known_plan_is_valid(plan):
    """R1: every plan in the table is valid."""
    assert is_valid_plan(plan)


@pytest.mark.parametrize("plan", ["GOLD", "basic", ""])
def test_r1_unknown_plan_is_invalid(plan):
    """R1: any other plan is invalid (names are exact)."""
    assert not is_valid_plan(plan)


def test_r2_extra_prices():
    """R2: the extras have the monthly prices per member of the table."""
    assert EXTRAS == {
        "GROUP_CLASSES": Decimal("15"),
        "PERSONAL_TRAINING": Decimal("25"),
        "SPA": Decimal("30"),
        "SPECIALIZED_PROGRAM": Decimal("40"),
    }
    assert PREMIUM_EXTRAS == {"SPA", "SPECIALIZED_PROGRAM"}


def test_r2_no_extras_is_valid():
    """R2: zero extras is allowed."""
    assert is_valid_extras("BASIC", [])


def test_r2_unknown_extra_is_invalid():
    """R2: an extra outside the table is invalid."""
    assert not is_valid_extras("PREMIUM", ["SAUNA"])


def test_r2_repeated_extra_is_invalid():
    """R2 (assumption): the same extra cannot be chosen twice."""
    assert not is_valid_extras("BASIC", ["GROUP_CLASSES", "GROUP_CLASSES"])


@pytest.mark.parametrize("plan", ["BASIC", "STANDARD"])
def test_r2_premium_extra_needs_premium_plan(plan):
    """R2: premium extras are invalid with a non-premium plan."""
    assert not is_valid_extras(plan, ["SPA"])


def test_r2_premium_extra_with_premium_plan_is_valid():
    """R2: premium extras are valid with the PREMIUM plan."""
    assert is_valid_extras("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM"])


def test_r2_has_premium_extra():
    """R2: premium detection, used later by the surcharge (R6)."""
    assert has_premium_extra(["GROUP_CLASSES", "SPA"])
    assert not has_premium_extra(["GROUP_CLASSES", "PERSONAL_TRAINING"])


@pytest.mark.parametrize("members", [1, 4])
def test_r3_valid_members(members):
    """R3: members is a whole number of at least 1."""
    assert is_valid_members(members)


@pytest.mark.parametrize("members", [0, -3, 1.5, "2", True])
def test_r3_invalid_members(members):
    """R3: zero, negatives, decimals, text and booleans are invalid."""
    assert not is_valid_members(members)


def test_valid_selection():
    """A known plan, valid extras and members make a valid selection."""
    assert is_valid_selection("PREMIUM", ["GROUP_CLASSES", "SPA"], 2)


@pytest.mark.parametrize(
    "plan, extras, members",
    [
        ("GOLD", [], 1),
        ("BASIC", ["SPA"], 1),
        ("BASIC", [], 0),
    ],
)
def test_invalid_selection(plan, extras, members):
    """One invalid part makes the whole selection invalid (R7: result -1)."""
    assert not is_valid_selection(plan, extras, members)
