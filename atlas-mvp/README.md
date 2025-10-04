# Atlas MVP

Welcome to **Atlas**, a friendly offline-first personal AI assistant. This repository ships a progressive, beginner-focused codebase that walks you from an empty folder to a working Streamlit + FastAPI stack backed by SQLite and local language models.

## Quickstart

```bash
make setup
make run
```

The commands above create a Python virtual environment, install dependencies, seed the SQLite database with demo content, and launch both the FastAPI backend (http://localhost:8000) and Streamlit UI (http://localhost:8501).

For step-by-step tutorials, check the [`docs/`](docs) directory starting with [`00_GETTING_STARTED.md`](docs/00_GETTING_STARTED.md).

## Why Atlas?

* **Offline-first:** Uses [Ollama](https://ollama.com/) by default so the core chat experience works without the cloud.
* **Beginner friendly:** Exhaustive comments, docstrings, and "BEGINNER TIP" notes.
* **Modular:** Backed by FastAPI services, a Streamlit front-end, and a lightweight plugin system.
* **Extensible:** Add new tools, models, or UI pages following the included guidance.

## Repository Tour

```
atlas-mvp/
  apps/ui_streamlit/   # Streamlit application with chat, tasks, notes, plugins pages
  apps/api_fastapi/    # FastAPI backend, services, routers, models, and tests
  data/                # SQLite storage folder and seed JSON files
  docs/                # Tutorials, architecture notes, troubleshooting, roadmap
  plugins/             # Example plugin contracts and implementations
  scripts/             # Handy scripts for bootstrapping, seeding, exporting, resetting
```

## Developing

1. Copy `.env.example` to `.env` and update values if desired.
2. Run `pre-commit install` to enable linting and formatting on commit.
3. Use `make format` and `make lint` to keep the code tidy.
4. Run `make test` for pytest-based smoke tests.

## License

MIT — see [`LICENSE`](LICENSE).
