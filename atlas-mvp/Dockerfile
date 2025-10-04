FROM python:3.11-slim

# BEGINNER TIP: Use a working directory inside the container to keep files organised.
WORKDIR /app

# Install system dependencies for audio (voice), sqlite, and build tools.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command launches the API. Use docker-compose to run UI as well.
CMD ["uvicorn", "apps.api_fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
