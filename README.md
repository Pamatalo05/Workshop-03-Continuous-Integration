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

## Team workflow

See [CONTRIBUTING.md](CONTRIBUTING.md) for roles, branches and the agreed function signatures.
