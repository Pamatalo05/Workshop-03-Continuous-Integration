"""Tests for the command line (R8)."""

import pytest

from gym_quote.cli import format_breakdown, main, parse_extras, parse_members, run
from gym_quote.quote import INVALID, build_quote


def fake_input(*answers):
    """Return a read function that gives the answers in order."""
    replies = iter(answers)
    return lambda _prompt: next(replies)


def test_r8_confirmed_quote_shows_each_step_and_returns_total():
    """R8: the breakdown is shown and 'y' returns the total."""
    output = []
    result = run(fake_input("PREMIUM", "GROUP_CLASSES, SPA", "2", "y"), output.append)
    assert result == 215
    assert "Subtotal: 230.00" in output
    assert "Group discount (R4): -23.00" in output
    assert "Special offer (R5): -20.00" in output
    assert "Premium surcharge (R6): +28.05" in output
    assert "Total: 215" in output
    assert output[-1] == "Result: 215"


def test_r8_answer_no_returns_minus_one():
    """R8: if the answer is no, the result is -1."""
    output = []
    assert run(fake_input("BASIC", "", "1", "n"), output.append) == INVALID
    assert output[-1] == "Result: -1"


def test_r8_invalid_selection_returns_minus_one_without_confirmation():
    """R7, R8: an invalid selection gives -1 and does not ask for confirmation."""
    output = []
    assert run(fake_input("BASIC", "SPA", "1"), output.append) == INVALID
    assert "Invalid selection." in output


def test_r8_input_is_not_case_sensitive():
    """R8 (assumption): the command line accepts lower case names and answers."""
    assert run(fake_input("basic", "group_classes", "3", "Y"), lambda _line: None) == 122


@pytest.mark.parametrize(
    "text, expected",
    [
        ("spa, group_classes", ["SPA", "GROUP_CLASSES"]),
        ("", []),
        (" , ", []),
    ],
)
def test_r8_parse_extras(text, expected):
    """R8: extras are comma separated; blank means none."""
    assert parse_extras(text) == expected


@pytest.mark.parametrize("text, expected", [(" 3 ", 3), ("abc", 0), ("1.5", 0), ("", 0)])
def test_r8_parse_members(text, expected):
    """R8: text that is not a whole number becomes 0, which is invalid (R3)."""
    assert parse_members(text) == expected


def test_r8_format_breakdown_ends_with_total():
    """R8: the last line of the breakdown is the rounded total."""
    assert format_breakdown(build_quote("BASIC", [], 1))[-1] == "Total: 30"


def test_r8_main_uses_keyboard_and_screen(monkeypatch, capsys):
    """R8: main() reads with input() and writes with print()."""
    monkeypatch.setattr("builtins.input", fake_input("BASIC", "", "1", "y"))
    assert main() == 30
    assert "Result: 30" in capsys.readouterr().out
