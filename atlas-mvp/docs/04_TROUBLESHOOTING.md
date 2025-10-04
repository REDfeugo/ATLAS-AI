# Troubleshooting Atlas

## API will not start

* Ensure you have run `make setup`.
* Delete the `data/storage/atlas.db` file and run `make seed` if migrations failed.
* Check `logs/atlas.log` for stack traces.

## Streamlit says "API unreachable"

* Confirm `make run` is running and that the API started on port 8000.
* If using Docker, verify the container ports are published (`docker ps`).
* Update `ATLAS_API_URL` environment variable when hosting on another machine.

## Ollama not found

* Install Ollama from https://ollama.com/ and run `ollama serve`.
* Change `MODEL_NAME` in `.env` to a model you have already pulled, e.g. `ollama pull llama3`.
* As a fallback, set `OPENAI_API_KEY`.

## Semantic search returns empty results

* Ensure you have at least one note or task saved.
* Run `python scripts/seed_data.py` to load demo notes and tasks.
* Confirm `sentence-transformers` installed correctly. The log warning indicates if a random fallback is used.

## Voice input issues

* Microphone access may require OS-level permissions.
* Verify `SpeechRecognition` and `PyAudio` dependencies. (On Linux, install `portaudio`.)
* The feature is optional; disable it if hardware support is unavailable.
