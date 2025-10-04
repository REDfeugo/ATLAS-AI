# Atlas Architecture Overview

Atlas consists of three major layers:

1. **Streamlit UI (`apps/ui_streamlit`)** — Presents chat, tasks, notes, and plugins pages.
2. **FastAPI backend (`apps/api_fastapi`)** — Hosts REST endpoints, services, and database models.
3. **SQLite storage (`data/storage/atlas.db`)** — Persists chat history, notes, tasks, embeddings, and plugin state.

## Request flow

```
Streamlit → FastAPI router → Service → SQLAlchemy models / LLM / Embeddings → Response
```

* Chat messages travel from the UI to `/llm/chat`, which logs the conversation and forwards it to the `LLMService`.
* Tasks and notes use CRUD routers (`/tasks`, `/notes`) that call into `TaskService` and `NoteService` for business logic.
* Semantic search sends payloads to `/memory/semantic_search`, which uses `EmbeddingService` to compute cosine similarity.

## Offline-first model handling

`LLMService` first attempts to use [Ollama](https://ollama.com/) via the Python client. If Ollama is unreachable, it falls back to OpenAI when `OPENAI_API_KEY` is set. The service returns clear guidance when neither option is available.

## Plugins

Plugins live in `plugins/<name>/` and require two files:

* `manifest.yaml` — Metadata including the entrypoint module.
* `<entrypoint>.py` — Exposes a `run(payload)` function executed by the API.

The plugin system loads manifests at runtime, stores enable/disable state in SQLite, and executes the function using `importlib`.

## Voice milestone

The optional v0.5 milestone adds speech recognition and text-to-speech using `SpeechRecognition` and `pyttsx3`. The Streamlit UI toggles these features; the backend exposes `/llm/voice_to_text` to capture microphone input.
