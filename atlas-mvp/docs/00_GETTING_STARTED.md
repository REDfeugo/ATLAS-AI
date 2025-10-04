# Getting Started with Atlas

Welcome to Atlas! This guide walks you from zero to a running local-first assistant.

## 1. Install prerequisites

* Python 3.11+
* [Ollama](https://ollama.com/) if you want fully offline chat
* (Optional) A working microphone if you plan to try voice commands

## 2. Clone and bootstrap

```bash
git clone <your-fork-url>
cd atlas-mvp
make setup
```

`make setup` creates a virtual environment, installs requirements, configures pre-commit hooks, and seeds the SQLite database with example notes and tasks.

## 3. Launch the stack

```bash
make run
```

This command launches:

* FastAPI backend at http://localhost:8000
* Streamlit UI at http://localhost:8501

Open the UI in your browser to start exploring.

## 4. Configure models

Atlas defaults to using the `llama3:instruct` Ollama model. If Ollama is not installed, you can supply an OpenAI API key instead:

1. Copy `.env.example` to `.env`
2. Set `OPENAI_API_KEY=sk-...`
3. Restart the app

The UI will show a helpful message if no model is reachable.

## 5. Next steps

* Read [`01_ARCHITECTURE.md`](01_ARCHITECTURE.md) for a systems overview.
* Explore the code in `apps/ui_streamlit` and `apps/api_fastapi`.
* Check [`05_PROGRESSIVE_MILESTONES.md`](05_PROGRESSIVE_MILESTONES.md) to follow the incremental roadmap.
