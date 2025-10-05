# Getting Started on Windows 11

Welcome to **ATLAS-AI**! This walkthrough assumes a Windows 11 HP EliteBook
830 G5 with 8 GB RAM. All commands run inside *Windows Terminal* or *PowerShell*.

## 1. Install prerequisites

1. **Python 3.11** – download from [python.org](https://www.python.org/downloads/) and
   tick *Add Python to PATH* during install.
2. **Git** – install the latest Git for Windows.
3. **Ollama** – download from [ollama.com](https://ollama.com/download) and restart once.
4. Optional but recommended: **Visual Studio Build Tools** for native deps.

## 2. Clone and bootstrap

```powershell
cd %USERPROFILE%\Dev
git clone https://github.com/your-handle/ATLAS-AI.git
cd ATLAS-AI
python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
make setup
```

`make setup` creates the virtualenv, installs dependencies, generates brand assets,
seeds the SQLite database with demo notes/tasks, and (optionally) indexes documents.

## 3. Pull the local model

```powershell
ollama pull llama3.2:3b
```

If you prefer a smaller model, adjust `MODEL_NAME` inside `.env`.

## 4. Launch the stack

```powershell
make run
```

This starts the FastAPI backend at `http://localhost:8000` and the Streamlit UI at
`http://localhost:8501`. When the UI loads you should see the black-and-gold brand
header, a LOCAL/CLOUD badge, and seeded demo content.

## 5. Verify voice & commands

* Visit **Voice & Control** page, click the **Push-to-talk** button, say a short
  phrase, and confirm the transcript is rendered. If Vosk is missing you will see a
  branded helper message.
* Open the **Command Line** page and run `app open notepad`. A preview appears and
  after confirmation the control service simulates the action.

## 6. Optional: enable OpenAI fallback

Edit `.env` and populate `OPENAI_API_KEY=sk-...`. Restart `make run` to expose the
CLOUD badge and fallback routing.

## 7. Next steps

* Read `docs/16_COMMAND_GRAMMAR.md` for the command DSL.
* Explore `docs/05_VOICE_PIPELINE.md` to swap wake-word engines.
* Run `pytest` from the repo root to execute smoke tests.
