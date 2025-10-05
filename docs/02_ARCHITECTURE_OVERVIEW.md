# Architecture Overview

```
+------------------+      HTTP      +----------------------+      SQLAlchemy
| Streamlit UI     | <------------> | FastAPI (apps/api_*) | <----------------+
|  - Chat          |                |  - Routers           |                  |
|  - Tasks/Notes   |                |  - Services          |                  |
|  - Voice/Control |                |  - Core (config/db)  |                  |
+------------------+                +----------------------+                  |
       ^   |                                                                       |
       |   v                                                                       v
   Local state (apps/ui_streamlit/utils/state.py)                           SQLite (data/atlas.db)
```

## Data flow

1. **Chat request** – Streamlit posts `/llm/chat` with current history.
2. **LLM service** – chooses Ollama or OpenAI, enforces rate limits, and returns the
   reply plus metadata.
3. **Memory service** – persists chat messages, tasks, notes, document embeddings.
4. **Planner/Control** – `/control/plan` turns natural language into steps, `/control/execute`
   dispatches tools via the skill registry and logs to `audit_events`.
5. **Voice** – `/voice/transcribe` decodes audio (Vosk) and returns transcripts.

## Module boundaries

* `apps/ui_streamlit/components` – reusable UI (brand header, message bubbles,
  permission badges, command help).
* `apps/ui_streamlit/utils` – API client, session state, audio helpers, localisation.
* `apps/api_fastapi/core` – configuration, logging, SQLAlchemy models, permissions,
  platform adapters.
* `apps/api_fastapi/services` – business logic for LLM, memory, planner, control,
  plugins, voice.
* `skills/windows` – implementation of safe Windows skills with simulated fallbacks.
* `skills/posix` – stubs documenting TODOs for macOS/Linux.

## Brand layer

* `.streamlit/config.toml` applies the black & gold theme across Streamlit pages.
* `brand/theme.css` adds reusable CSS classes for chat bubbles, cards, and callouts.
* `apps/api_fastapi/core/banner.py` prints the CLI banner using ANSI gold when the API
  boots.
