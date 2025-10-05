# Testing and QA

## Automated tests

Run `pytest` from the repo root. Current smoke suite covers:

* Health endpoint
* Memory semantic search (notes/tasks/documents)
* Planner output heuristics
* Command parser plan generation

Add new tests under `apps/api_fastapi/tests/` and ensure they run offline.

## Manual QA checklist

1. `make setup && make run`
2. Visit UI homepage – confirm brand header, LOCAL badge, seeded data.
3. Chat with `/ask "What's on my task list?"` – expect response referencing tasks.
4. Run command `app open notepad` – verify preview + simulated execution.
5. Voice page – hold push-to-talk, speak, confirm transcript appears.
6. Planner scenario – submit example prompt from README, confirm confirmation request for
   file creation.
7. Plugins page – enable example plugin and run the default payload.
8. Notes page – create a note, ensure it appears in semantic search results.
9. Run `make test` – expect all tests pass.
10. Stop services and run `python scripts/index_documents.py` to ensure indexing completes.
