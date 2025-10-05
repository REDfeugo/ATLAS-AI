# Deploy Options

## Windows service

Use `nssm` or Windows Task Scheduler to run `make run` on login. Ensure the virtualenv is
activated within the script (call `.venv\Scripts\activate`).

## Desktop shell (future)

A Tauri wrapper can embed the Streamlit UI. The roadmap in `docs/13_ROADMAP_MILESTONES.md`
flags this as a later milestone once cross-platform skills ship.

## Docker (optional)

`Dockerfile` and `docker-compose.yml` provide a low-footprint container with two services:

* `api` – uvicorn + FastAPI
* `ui` – Streamlit

On an 8 GB machine Docker adds overhead, so use it only for testing remote deployment.
After `docker-compose up --build`, forward host audio manually if voice features are needed.

## Remote access

Expose the UI securely using `ssh -L 8501:localhost:8501 user@host` rather than opening
public ports. Plugins and skills remain local to the remote machine.
