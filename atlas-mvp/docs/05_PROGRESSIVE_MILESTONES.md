# Progressive Milestones

Atlas grows capability in stages so you can learn step-by-step.

## v0.1 – Core Chat + Health

* Streamlit chat page wired to `/llm/chat`
* Health endpoint and sidebar status
* Ollama-first model selection with OpenAI fallback guidance

## v0.2 – Memory (SQLite)

* Persist chat history, tasks, and notes using SQLAlchemy
* Embedding table in SQLite storing vectors as blobs
* Semantic search endpoint `/memory/semantic_search`

## v0.3 – Tasks & Notes

* CRUD endpoints and UI pages for tasks and notes
* Tagging, due dates, and quick recall in UI
* Database seeds for example notes/tasks

## v0.4 – Plugin System

* `plugins/<name>` folders with manifest + Python module
* API endpoints to list, toggle, and run plugins
* Streamlit page to enable/disable and execute plugins

## v0.5 – Voice (optional)

* `/llm/voice_to_text` endpoint using `SpeechRecognition`
* Streamlit controls to record microphone input and toggle text-to-speech
* `pyttsx3` ready for local playback experiments
