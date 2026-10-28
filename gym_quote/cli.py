"""Command line for the gym membership quote (R8).

Only input and output live here; every calculation is in gym_quote.quote.
Run it with: python -m gym_quote.cli
"""

from gym_quote.catalog import EXTRAS, PLANS
from gym_quote.quote import INVALID, build_quote

YES_ANSWERS = frozenset({"y", "yes"})


def parse_extras(text):
    """Turn 'spa, group_classes' into ['SPA', 'GROUP_CLASSES']; blank means none."""
    return [item.strip().upper() for item in text.split(",") if item.strip()]


def parse_members(text):
    """Return the number of members, or 0 (invalid) if the text is not a whole number."""
    try:
        return int(text.strip())
    except ValueError:
        return 0


def format_breakdown(quote):
    """Return the lines that show the subtotal, each discount, the surcharge and the total."""
    return [
        f"Subtotal: {quote.subtotal:.2f}",
        f"Group discount (R4): -{quote.group_discount:.2f}",
        f"Special offer (R5): -{quote.special_offer:.2f}",
        f"Premium surcharge (R6): +{quote.premium_surcharge:.2f}",
        f"Total: {quote.total}",
    ]


def run(read, write):
    """Ask for plan, extras and members, show the breakdown and ask for confirmation.

    Return the total, or -1 if the selection is invalid or the user cancels (R7, R8).
    """
    write(f"Plans: {', '.join(PLANS)}")
    plan = read("Plan: ").strip().upper()
    write(f"Extras: {', '.join(EXTRAS)} (comma separated, blank for none)")
    extras = parse_extras(read("Extras: "))
    members = parse_members(read("Members: "))

    quote = build_quote(plan, extras, members)
    if quote is None:
        write("Invalid selection.")
        write(f"Result: {INVALID}")
        return INVALID

    for line in format_breakdown(quote):
        write(line)
    answer = read("Confirm? (y/n): ").strip().lower()
    result = quote.total if answer in YES_ANSWERS else INVALID
    write(f"Result: {result}")
    return result


def main():
    """Run the command line with the keyboard and the screen; return the result."""
    return run(input, print)


if __name__ == "__main__":
    main()
