# Contributing

## Workflow

1. Update `main`: `git checkout main && git pull`.
2. Create a branch: `git checkout -b feature/<name>`.
3. Commit small changes with clear messages, run `pytest` and `pylint` locally.
4. Push and open a pull request to `main`. Another member reviews it.
5. Merge only when GitHub Actions is green. Wait for the Jenkins build before the next merge.

## Roles

| Role | Owns |
| --- | --- |
| Repository lead | Repository, branches, reviews and merges, command line (R8) |
| Automation lead | Jenkins, webhook, GitHub Actions, tests of the worked examples |
| Developer A | R1, R2, R3, R7 and their tests |
| Developer B | R4, R5, R6 and their tests |

## Agreed function signatures

Amounts are `Decimal` until the final rounding, so no cents are lost. Developer B's
functions receive an amount and return an amount, so nobody waits for anybody.

| Module | Function | Owner | Req. |
| --- | --- | --- | --- |
| `gym_quote/catalog.py` | `PLANS`, `EXTRAS` (`dict[str, Decimal]`), `PREMIUM_EXTRAS: frozenset[str]` | Developer A | R1, R2 |
| `gym_quote/catalog.py` | `is_valid_selection(plan, extras, members) -> bool` | Developer A | R1, R2, R3 |
| `gym_quote/quote.py` | `calculate_subtotal(plan, extras, members) -> Decimal` | Developer A | R3 |
| `gym_quote/quote.py` | `round_half_up(amount) -> int` | Developer A | R7 |
| `gym_quote/adjustments.py` | `apply_group_discount(amount, members) -> Decimal` | Developer B | R4 |
| `gym_quote/adjustments.py` | `apply_special_offer(amount) -> Decimal` | Developer B | R5 |
| `gym_quote/adjustments.py` | `apply_premium_surcharge(amount, has_premium) -> Decimal` | Developer B | R6 |
| `gym_quote/quote.py` | `build_quote(plan, extras, members) -> QuoteBreakdown or None` | Developer B | R4 to R7 |
| `gym_quote/quote.py` | `calculate_total(plan, extras, members) -> int` | Developer A | R7 |
| `gym_quote/cli.py` | `main() -> int` (input/output only, no calculation) | Repository lead | R8 |

Notes:

- `round_half_up` must not use the built-in `round` (it rounds half to even); it uses `decimal.Decimal` with `ROUND_HALF_UP`.
- Invalid selections and cancelled quotes return `-1` (`INVALID` in `gym_quote/quote.py`).
- The worked-examples table of the assignment lives in `tests/test_workshop_table.py` (Automation lead).

## Assumptions

- Plan and extra names are exact (upper case) in the functions; the command line converts what the user types to upper case.
- The same extra cannot be chosen twice.
- The number of members is a whole number of at least 1; any other input is invalid.
- In the command line, only `y` or `yes` confirms the quote; any other answer cancels it (result `-1`).
