# Atlas / ARES (Local, Offline-First)

Atlas ARES is a desktop-friendly AI operator console that runs entirely on a local machine. It couples a Streamlit UI with a FastAPI backend, a SQLite data store, and optional plugins to orchestrate an offline-first workflow. Atlas ARES talks to local large language models via [Ollama](https://ollama.ai/) and augments responses with retrieval-augmented generation (RAG) over locally stored markdown files.

```
+-----------------+        +--------------------+        +-------------------+
| Streamlit UI    | <----> | FastAPI (JWT auth) | <----> | SQLite + JSONL    |
| Tabs & feedback |        | Routes: auth, RAG  |        | Policy, logs, RAG |
+-----------------+        +--------------------+        +-------------------+
         |                             |                          |
         v                             v                          v
  Local browser                 Ollama HTTP API           Vector store (FAISS
                                                          with Annoy/Sklearn fallback)
```

## Key Features

- Offline-first assistant console optimised for Windows laptops (HP EliteBook class hardware).
- JWT-protected FastAPI backend with promotion approvals, feedback, planner, and RAG endpoints.
- SQLite persistence, append-only JSONL API logs, and epsilon-greedy policy tracking.
- Streamlit operator UI for auth, approvals, logs, chat, RAG, and voice stubs.
- Retrieval augmented generation over local markdown documents with FAISS primary and graceful Annoy/Scikit-learn fallbacks.
- Planner/executor loop with guardrails to keep automation bounded.
- Automated tests, linting, and CI to maintain quality.

## Prerequisites

- Python 3.11
- Git
- [Ollama](https://ollama.ai) installed locally with at least one model pulled (e.g. `mistral` or `qwen2`)
- (Optional) sentence-transformers model cache; downloaded automatically on first run

## Setup

1. **Clone and enter the project**
   ```powershell
   git clone <repo-url>
   cd atlas-ares
   ```
2. **Create a virtual environment**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
3. **Install dependencies**
   ```powershell
   pip install -r requirements\base.txt
   pip install -r requirements\rag.txt    # optional but recommended
   pip install -r requirements\voice.txt  # optional stubs
   pip install -r requirements\dev.txt    # tooling/tests
   ```
4. **Configure environment**
   ```powershell
   Copy-Item .env.example .env
   # Update JWT secret and any paths if needed
   ```
5. **Prepare Ollama** (example models)
   ```powershell
   ollama pull mistral
   ollama pull qwen2:0.5b
   ```

## Running Atlas ARES

Start the FastAPI backend (default port 8000):
```powershell
uvicorn api.server:app --reload --host 0.0.0.0 --port 8000
```

Launch the Streamlit UI (default port 8501):
```powershell
streamlit run ui/app.py --server.port 8501
```

The UI defaults to `http://127.0.0.1:8000` for API calls; adjust `ARES_API_URL` if you expose the API on another interface.

## Creating an Admin User

Accounts created via `/auth/signup` are regular users. To promote an account to admin, run the following SQLite one-liner after creating the user:

```powershell
python -c "import sqlite3; conn = sqlite3.connect('data/ares.db'); conn.execute('UPDATE users SET role = ? WHERE email = ?', ('admin', 'user@example.com')); conn.commit(); conn.close()"
```

Replace `user@example.com` with the target email.

## Retrieval-Augmented Generation (RAG)

1. Place markdown knowledge base files under `data/docs/`.
2. Call `/rag/index` (from UI or API) to embed and index documents. Embeddings are stored in `data/embeddings/` and metadata in SQLite.
3. Ask questions through `/rag/ask` or the Streamlit RAG tab. Responses include citations with document paths and snippets.
4. If FAISS is unavailable, Atlas ARES transparently falls back to Annoy or Scikit-learn for vector search.

## Planner Usage

Send a POST request to `/plan/execute` with `{ "goal": "Describe quarterly OKRs" }`. The planner runs a bounded step loop using guardrailed tools and returns the intermediate steps plus a final summary. Set `dry_run=true` to review tool selection without executing side effects.

## Feedback & Bandit Policy

The `/feedback/record` endpoint stores task outcomes and updates an epsilon-greedy policy in SQLite. The AI chat route reads the policy to balance exploration vs. exploitation across configured local models.

## Tests & CI

Automated checks include unit tests, linting, and formatting. To run locally:

```powershell
pytest
ruff check .
black --check .
isort --check-only .
```

GitHub Actions replicates these steps in `.github/workflows/ci.yml`.

## Known Limitations

- Quantised models (e.g. `mistral:7b-instruct-q4`) are recommended for 8 GB RAM systems.
- Initial embedding runs can be slow; cached models reduce subsequent latency.
- The sample planner uses simple heuristics; extend with plugins for complex tasks.
- Voice endpoints are stubs; integrate whisper.cpp or Coqui-TTS for production use.

## Troubleshooting

- **Ollama connection errors** – ensure `ollama serve` is running and `OLLAMA_HOST` matches your setup.
- **FAISS missing** – install `faiss-cpu` via `pip install -r requirements/rag.txt`. Until then, Atlas ARES switches to the fallback vector backend automatically.
- **Large logs** – rotate or archive `logs/api.jsonl` periodically.

## License

Atlas ARES is released under the [MIT License](LICENSE).
