# Contributing to agent-events

Thank you for considering a contribution! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/darshjme-codes/agent-events
cd agent-events
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
python -m pytest tests/ -v
```

All tests must pass before submitting a pull request.

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/).
- Use type annotations everywhere.
- Keep zero runtime dependencies.

## Submitting Changes

1. Fork the repo and create a feature branch: `git checkout -b feat/my-feature`.
2. Make your changes with tests.
3. Update `CHANGELOG.md` under `[Unreleased]`.
4. Open a pull request with a clear description.

## Reporting Bugs

Use [GitHub Issues](https://github.com/darshjme-codes/agent-events/issues). Include:
- Python version
- Minimal reproducible example
- Expected vs actual behaviour

## Code of Conduct

All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).
