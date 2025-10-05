# ATLAS-AI

Atlas / ARES is an offline-first personal AI assistant designed for novice "vibe coders".
The stack pairs a Streamlit UI with a FastAPI backend, SQLite memory, local Ollama LLM,
optional OpenAI fallback, Windows automation skills, voice controls, and a black & gold
brand system.

## Highlights

* **Local chat** via Ollama `llama3.2:3b` with automatic cloud fallback when `OPENAI_API_KEY`
  is set.
* **Command interface** – CLI-style page and chat slash commands that map to planner steps.
* **Voice assistant** – push-to-talk button, optional wake-word, Vosk transcription, and
  pyttsx3 "professional butler" TTS.
* **Windows control** – safe tool registry to open apps, adjust volume, manipulate files,
  edit clipboard, control the browser, and capture screenshots.
* **Memory & RAG** – tasks, notes, chats, and optional Documents indexing stored in SQLite
  with sentence-transformers embeddings.
* **Plugins** – allowlisted Python tools with permission tiers and audit logging.
* **Brand** – gold-on-black theme, CLI banner, and reproducible SVG-to-PNG asset pipeline.

## Quick start (Windows 11)

```powershell
# clone and enter
cd %USERPROFILE%\Dev
git clone https://github.com/your-handle/ATLAS-AI.git
cd ATLAS-AI

# bootstrap
python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
make setup

# pull local model
ollama pull llama3.2:3b

# run ui + api
make run
```

Visit `http://localhost:8501` (UI) and `http://localhost:8000/docs` (API).

## Command samples

```
app open notepad
vol set 60
file new "%USERPROFILE%\Desktop\hello.txt" --content "Hello Atlas"
web open https://github.com/
note add "Standup at 9am — talk Atlas planner"
task add "Renew domain" --due 2025-10-10 --tags ops,urgent
plan "Open Notepad, type 'Hello Atlas', save to Desktop as hello.txt, then read it back"
```

## Project structure

See `docs/02_ARCHITECTURE_OVERVIEW.md` for a deep dive. Top-level directories:

```
apps/               # Streamlit UI + FastAPI backend
brand/              # SVG assets and theme.css
skills/             # Windows skills + POSIX stubs
data/               # Seeds, storage, logs, indices
scripts/            # Bootstrap, seeding, asset builder, indexing
docs/               # Beginner-friendly documentation set
```

## Testing

```
.\.venv\Scripts\activate
pytest
```

Smoke tests cover health, memory, planner, and command parsing.

## Contributing

1. Create a branch from `work`.
2. Run `make format` and `make lint` before committing.
3. Include documentation updates (`docs/*`) when adding features.
4. Ensure optional dependencies degrade gracefully (catch ImportError).

## License

MIT – see `LICENSE`.
