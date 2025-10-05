# Memory and Embeddings

Atlas stores structured and vector data inside `data/atlas.db` using SQLAlchemy.

## Tables

| Table            | Purpose                                   |
|------------------|-------------------------------------------|
| `chat_messages`  | Conversation history for recall           |
| `tasks`          | Task records with JSON-encoded tags       |
| `notes`          | Note records with JSON-encoded tags       |
| `embeddings`     | Vector store mapping `item_type` + `id`   |
| `document_chunks`| Indexed chunks from Documents folder      |
| `audit_events`   | Planner execution log                     |

## Embedding pipeline

`EmbeddingService` loads `all-MiniLM-L6-v2` (or a fallback). Vectors are stored as
`np.float32` arrays and converted to BLOB via `tobytes()`.

```python
vector = embed_service.embed([text])[0]
record = models.Embedding(item_type="note", item_id=note.id, vector=vector.tobytes())
```

Cosine similarity is computed manually:

```python
def cosine_similarity(a, b):
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) or 1.0
    return float(np.dot(a, b) / denom)
```

## Semantic search flow

1. UI posts `/memory/semantic_search` with `{query, top_k}`.
2. `MemoryService` embeds the query, iterates stored vectors, sorts by similarity.
3. Results include notes, tasks, and optional document chunks with `source_path`.

## Documents ingestion

`scripts/index_documents.py` scans `%USERPROFILE%\Documents` (configurable), splits
`.txt` files into ~400 character chunks, and calls `MemoryService.upsert_document_chunk`.
Set `INDEX_DOCUMENTS=true` in `.env` to run the job during `make setup` or manually via
`make index-docs`.

## RAG quickstart

Use the command page to run:

```
ask "Summarize the last 5 notes"
```

The planner hits the `create_note` tool when needed; semantic search powers the recall
context passed to the LLM service.
