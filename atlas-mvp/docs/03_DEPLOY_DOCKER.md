# Deploying Atlas with Docker

Running Atlas via Docker keeps dependencies isolated and reproducible.

## 1. Copy environment variables

```
cp .env.example .env
```

Update `.env` if you want to override defaults like `MODEL_NAME` or `DB_PATH`.

## 2. Build and start containers

```
docker-compose up --build
```

This launches two services:

* `api` — FastAPI backend on port 8000
* `ui` — Streamlit frontend on port 8501

Both share the `./data/storage` folder for persistence.

## 3. Connect to Ollama

If your Ollama service runs on the host machine, add this to `.env` before starting Docker:

```
OLLAMA_HOST=http://host.docker.internal:11434
```

This instructs the container to reach the host network.

## 4. Stop services

```
docker-compose down
```

The SQLite database remains on your host inside `data/storage/`.
