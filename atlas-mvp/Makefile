# BEGINNER TIP: `make <target>` runs the commands defined below. Targets chain together
# to create a friendly developer experience.

PYTHON=python3
PIP=$(PYTHON) -m pip
VENV?=.venv
ACTIVATE=. $(VENV)/bin/activate

setup: ## Create virtualenv, install dependencies, run pre-commit, seed DB
@if [ ! -d $(VENV) ]; then $(PYTHON) -m venv $(VENV); fi
$(ACTIVATE) && $(PIP) install --upgrade pip
$(ACTIVATE) && $(PIP) install -r requirements.txt
$(ACTIVATE) && pre-commit install
$(ACTIVATE) && bash scripts/dev_bootstrap.sh
$(ACTIVATE) && python scripts/seed_data.py

run: ## Run both API and UI using separate terminals via streamlit/uvicorn
$(ACTIVATE) && uvicorn apps.api_fastapi.main:app --reload & \
API_PID=$$!; \
$(ACTIVATE) && streamlit run apps/ui_streamlit/Home.py --server.port 8501; \
kill $$API_PID

run-api: ## Only run the FastAPI backend
$(ACTIVATE) && uvicorn apps.api_fastapi.main:app --reload

run-ui: ## Only run the Streamlit frontend
$(ACTIVATE) && streamlit run apps/ui_streamlit/Home.py --server.port 8501

format: ## Apply formatting using black and isort
$(ACTIVATE) && black .
$(ACTIVATE) && isort .

lint: ## Run lint checks via flake8
$(ACTIVATE) && flake8 .

test: ## Run pytest suite
$(ACTIVATE) && pytest

seed: ## Re-seed the database with demo data
$(ACTIVATE) && python scripts/seed_data.py

reset-db: ## Reset the SQLite database
$(ACTIVATE) && python scripts/reset_db.py

export-db: ## Export database rows to JSON
$(ACTIVATE) && python scripts/export_db.py

clean: ## Remove the virtual environment
rm -rf $(VENV)

# Docker targets keep the same offline-friendly approach.
docker-up: ## Build and start the stack using docker-compose
docker-compose up --build -d

docker-down: ## Stop Docker containers
docker-compose down

.PHONY: setup run run-api run-ui format lint test seed reset-db export-db clean docker-up docker-down
