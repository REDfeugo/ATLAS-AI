# API Reference

## Health

`GET /health`

```json
{
  "status": "ok",
  "versions": {"python": "3.11", "api": "0.7", "model": "llama3.2:3b"},
  "checks": {"ollama": {"configured": true}, "openai": {"configured": false}}
}
```

## Chat

`POST /llm/chat`

Request:
```json
{"message": "Hello", "history": [], "mode": "auto"}
```

Response:
```json
{"reply": "Hi!", "tokens": 3, "model_used": "llama3.2:3b"}
```

## Memory search

`POST /memory/semantic_search`

```json
{"query": "Atlas", "top_k": 5}
```

Returns `{ "results": [...] }` with `type` in `note|task|document`.

## Tasks / Notes

CRUD endpoints follow REST conventions: `GET /tasks`, `POST /tasks`, `PUT /tasks/{id}`.
Payloads match `apps/api_fastapi/core/schemas.py` models.

## Plugins

* `GET /plugins` – list descriptors.
* `POST /plugins/toggle` – `{ "name": str, "enabled": bool }`.
* `POST /plugins/run` – `{ "name": str, "payload": dict }` returning `{ "result": any, "logs": list }`.

## Control

* `POST /control/plan` – `{ "query": str }` → plan JSON.
* `POST /control/execute` – `{ "plan": PlanResponse, "confirm_token": str|null }`.

## Voice

`POST /voice/transcribe` – `{ "audio_base64": "...", "lang": "en" }` → transcript.

## Commands

`POST /commands/parse` – `{ "text": "app open notepad" }` returns mode, preview, and plan/action.

## Curl examples

```powershell
curl -X POST http://localhost:8000/control/plan -H "Content-Type: application/json" \
  -d '{"query":"Open Notepad"}'

curl -X POST http://localhost:8000/commands/parse -H "Content-Type: application/json" \
  -d '{"text":"file new demo.txt --content \"Hello\""}'
```
