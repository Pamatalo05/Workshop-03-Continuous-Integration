# Workshop-03-Continuous-Integration

Gym Membership Quote — ESPOL, Software Engineering II, Continuous Integration workshop (2026).

A command-line application that quotes the monthly cost of a gym membership.
Jenkins runs the tests on every push to `main`; GitHub Actions runs pytest and
pylint on every pull request to `main`.

## Run locally

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest
pylint $(git ls-files '*.py')
```

## Run the command line

```bash
python -m gym_quote.cli
```

Example:

```text
Plans: BASIC, STANDARD, PREMIUM
Plan: premium
Extras: GROUP_CLASSES, PERSONAL_TRAINING, SPA, SPECIALIZED_PROGRAM (comma separated, blank for none)
Extras: spa, group_classes
Members: 2
Subtotal: 230.00
Group discount (R4): -23.00
Special offer (R5): -20.00
Premium surcharge (R6): +28.05
Total: 215
Confirm? (y/n): y
Result: 215
```

## Project structure

| Path | Content | Requirements |
| --- | --- | --- |
| `gym_quote/catalog.py` | Plans, extras, premium extras and selection validation | R1, R2, R3 |
| `gym_quote/adjustments.py` | Group discount, special offer and premium surcharge | R4, R5, R6 |
| `gym_quote/quote.py` | Subtotal, breakdown, half-up rounding and final result | R3, R7 |
| `gym_quote/cli.py` | Input and output only: asks, shows the breakdown, confirms | R8 |
| `tests/` | Unit tests per requirement; the workshop table in `test_workshop_table.py` | R9 |
| `.github/workflows/ci.yml` | GitHub Actions: pytest and pylint on every pull request to `main` | — |
| `Dockerfile` | Jenkins image with Python for the Jenkins job | — |

## Assumptions

- Plan and extra names are exact (upper case) in the functions; the command line converts what the user types to upper case.
- The same extra cannot be chosen twice.
- The number of members is a whole number of at least 1; any other input is invalid.
- Only `y` or `yes` confirms the quote; any other answer cancels it and the result is `-1`.
- Amounts are kept as `Decimal` and rounded half up only at the end (122.5 → 123).

## Team workflow

See [CONTRIBUTING.md](CONTRIBUTING.md) for roles, branches and the agreed function signatures.
