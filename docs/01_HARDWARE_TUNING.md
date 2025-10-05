# Hardware Tuning on an 8 GB Laptop

Atlas targets an HP EliteBook 830 G5 (Intel i5-8250U, 4 cores / 8 threads). Use
these tactics to keep the experience smooth:

## Model selection

* Default: `llama3.2:3b` Q4 – ~4.2 GB VRAM-equivalent. Works on CPU with ~4 GB RAM.
* Alternative: `phi3:mini` for faster responses with slightly smaller context.
* If memory pressure spikes, edit `.env` `MODEL_NAME` to a 2-3B quant and restart.

## Conserve RAM

* Close heavyweight apps (Teams, Chrome with >10 tabs) before launching `make run`.
* Use Windows *Game Mode* to reduce background tasks.
* Disable real-time antivirus scanning for the project directory if corporate policy
  allows, otherwise add an exclusion for `ATLAS-AI` to reduce file-lock contention.

## Thread and batch tuning

* Ollama respects `OLLAMA_NUM_THREADS`. Set it to `4` to map to the CPU core count:
  ```powershell
  setx OLLAMA_NUM_THREADS 4
  ```
* For embeddings, the `sentence-transformers` model is CPU friendly. If inference is
  still slow, set `EMBED_MODEL_NAME=bge-small-en` in `.env`.

## Voice pipeline performance

* Vosk small-en model stays below 50 MB. For multilingual support switch to
  `vosk-model-small-multilingual` and update `VOICE_LANG` accordingly.
* If microphone latency is high, reduce the chunk size in
  `apps/ui_streamlit/utils/audio_io.py`.

## When to use the cloud fallback

* Long-form reasoning (>1500 tokens) or high-latency tasks: toggle to CLOUD mode to
  send the request through OpenAI (requires `OPENAI_API_KEY`).
* Keep a tight budget by reading the usage metrics shown in the Voice & Control page.
