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

Amounts are `float` until the final rounding. Developer B's functions receive an
amount and return an amount, so nobody waits for anybody.

| Module | Function | Owner | Req. |
| --- | --- | --- | --- |
| `gym_quote/catalog.py` | `PLANS: dict[str, int]`, `EXTRAS: dict[str, int]`, `PREMIUM_EXTRAS: frozenset[str]` | Developer A | R1 |
| `gym_quote/pricing.py` | `is_valid_selection(plan: str, extras: list[str], members: int) -> bool` | Developer A | R1, R2, R3 |
| `gym_quote/pricing.py` | `calculate_subtotal(plan: str, extras: list[str], members: int) -> float` | Developer A | R3 |
| `gym_quote/pricing.py` | `round_half_up(amount: float) -> int` | Developer A | R7 |
| `gym_quote/discounts.py` | `apply_group_discount(amount: float, members: int) -> float` | Developer B | R4 |
| `gym_quote/discounts.py` | `apply_special_offer(amount: float) -> float` | Developer B | R5 |
| `gym_quote/discounts.py` | `apply_premium_surcharge(amount: float, has_premium: bool) -> float` | Developer B | R6 |
| `gym_quote/quote.py` | `calculate_quote(plan: str, extras: list[str], members: int) -> QuoteBreakdown` | Developer A | R7 |
| `gym_quote/cli.py` | `main() -> int` (input/output only, no calculation) | Repository lead | R8 |

Notes:

- `round_half_up` must not use the built-in `round` (it rounds half to even); use `decimal.Decimal` with `ROUND_HALF_UP`.
- Invalid selections and cancelled quotes return `-1` (`INVALID_RESULT`).
- The worked-examples table of the assignment lives in `tests/test_worked_examples.py` (Automation lead).
