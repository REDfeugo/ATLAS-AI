# Contributing to Atlas ARES

Thanks for your interest in improving Atlas ARES! This document outlines the basics for contributing safely in an offline-first environment.

## Development Workflow

1. Fork the repository or create a branch.
2. Create a Python 3.11 virtual environment.
3. Install dependencies from `requirements/dev.txt`.
4. Copy `.env.example` to `.env` and adjust values.
5. Run `pre-commit install` to enable formatting hooks.
6. Run `pytest` locally before submitting changes.

## Coding Standards

- Follow the existing project layout; keep modules small and well documented.
- Use `ruff`, `black`, and `isort` for linting/formatting.
- Add or update tests with each change when possible.
- Prefer dependency-injected services for easier testing.

## Commit Messages & Pull Requests

- Write clear commit messages summarising the change.
- Provide context and testing evidence in pull requests.
- Update documentation or configuration files when behaviour changes.

## Reporting Issues

When filing an issue, include:

- The OS and Python version.
- Steps to reproduce the problem.
- Any relevant logs from `logs/api.jsonl` (redact secrets).

## Code of Conduct

All contributors must abide by the [Code of Conduct](CODE_OF_CONDUCT.md).
