# Security and Privacy

* **Local-first** – No network calls are made unless you set `OPENAI_API_KEY`. All data
  stays on disk under `data/`.
* **Logs** – Sensitive arguments are summarised before entering `audit_events`. Full tool
  arguments are stored as JSON in SQLite but never transmitted externally.
* **Rate limiting** – `SlidingWindowRateLimiter` throttles chat requests per minute to
  prevent runaway loops.
* **Permissions** – High-risk tools require confirmation. Set `DEFAULT_PERMISSION_TIER`
  to `never` for extra caution.
* **Data retention** – Delete `data/atlas.db` to wipe history. `make reset-db` recreates
  the file with seeds.
* **Brand assets** – Stored as SVG and generated locally via `scripts/build_assets.py` to
  avoid licensing issues with binary assets.
* **Voice** – Audio is processed in-memory and discarded after transcription.
* **Clipboard** – Write operations require confirmation and are logged.
