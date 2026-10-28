"""Worked examples from the workshop statement (R9).

Every row of the table in the assignment must give the expected monthly total.
"""

import pytest

from gym_quote.quote import INVALID, calculate_total

WORKSHOP_TABLE = [
    ("BASIC", [], 1, 30),
    ("STANDARD", ["PERSONAL_TRAINING"], 1, 70),
    ("BASIC", ["GROUP_CLASSES"], 2, 81),
    ("BASIC", ["GROUP_CLASSES"], 3, 122),
    ("STANDARD", ["GROUP_CLASSES", "PERSONAL_TRAINING"], 4, 286),
    ("PREMIUM", ["GROUP_CLASSES", "SPA"], 2, 215),
    ("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM"], 3, 412),
    ("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM", "PERSONAL_TRAINING"], 4, 626),
    ("BASIC", ["SPA"], 1, INVALID),
    ("GOLD", [], 1, INVALID),
    ("BASIC", [], 0, INVALID),
]


@pytest.mark.parametrize("plan, extras, members, expected", WORKSHOP_TABLE)
def test_r9_workshop_table(plan, extras, members, expected):
    """R9: each row of the workshop table gives its expected total."""
    assert calculate_total(plan, extras, members) == expected
