# Troubleshooting

| Symptom | Fix |
|---------|-----|
| UI shows "API unreachable" | Ensure `make run` is active. Check firewall prompts and allow Python/uvicorn. |
| Ollama errors (`connection refused`) | Start `ollama serve` manually or reinstall; verify `OLLAMA_HOST` in `.env`. |
| Vosk transcription empty | Confirm microphone permissions in Windows Privacy settings and that the model path exists. |
| pywinauto ImportError | Install `pip install pywinauto` inside the virtualenv and restart. |
| Playwright missing browsers | Run `.venv/Scripts/playwright install` to download Chromium. |
| Streamlit theme missing | Delete `.streamlit/config.toml` override in your profile; repo version re-applies brand colors. |
| CLI banner garbled | Use Windows Terminal or disable legacy console rendering. |
| `pip install` fails on optional deps | Re-run `make setup` after installing Visual C++ Build Tools; see `docs/01_HARDWARE_TUNING.md`. |

## Logs

* API logs rotate under `data/logs/` (ignored by git).
* Streamlit outputs to the terminal where `make run` executed.

## Resetting

* `make reset-db` – drops and recreates SQLite with fresh seeds.
* `make seed` – re-imports `data/seeds/*.json`.
* Delete `.venv` and rerun `make setup` for a clean reinstall.
