"""Catalog of plans and extras, and selection validation (R1, R2, R3)."""

from decimal import Decimal

PLANS = {
    "BASIC": Decimal("30"),
    "STANDARD": Decimal("45"),
    "PREMIUM": Decimal("70"),
}

EXTRAS = {
    "GROUP_CLASSES": Decimal("15"),
    "PERSONAL_TRAINING": Decimal("25"),
    "SPA": Decimal("30"),
    "SPECIALIZED_PROGRAM": Decimal("40"),
}

PREMIUM_EXTRAS = frozenset({"SPA", "SPECIALIZED_PROGRAM"})
PREMIUM_PLAN = "PREMIUM"


def is_valid_plan(plan):
    """Return True if the plan exists in the catalog (R1)."""
    return plan in PLANS


def has_premium_extra(extras):
    """Return True if the selection includes at least one premium extra."""
    return any(extra in PREMIUM_EXTRAS for extra in extras)


def is_valid_extras(plan, extras):
    """Return True if every extra exists, none repeats, and premium
    extras are only chosen with the PREMIUM plan (R2)."""
    if len(set(extras)) != len(extras):
        return False
    if any(extra not in EXTRAS for extra in extras):
        return False
    return plan == PREMIUM_PLAN or not has_premium_extra(extras)


def is_valid_members(members):
    """Return True if members is a whole number of at least 1 (R3)."""
    return isinstance(members, int) and not isinstance(members, bool) and members >= 1


def is_valid_selection(plan, extras, members):
    """Return True if plan, extras and members are all valid (R1, R2, R3).

    An invalid selection makes the result -1 (R7).
    """
    return (
        is_valid_plan(plan)
        and is_valid_extras(plan, extras)
        and is_valid_members(members)
    )
