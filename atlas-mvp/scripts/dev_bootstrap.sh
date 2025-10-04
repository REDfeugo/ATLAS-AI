#!/usr/bin/env bash
set -euo pipefail

# BEGINNER TIP: This script keeps initial setup simple and repeatable.
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
DATA_DIR="$PROJECT_ROOT/data/storage"

mkdir -p "$DATA_DIR"

if [ ! -f "$PROJECT_ROOT/.env" ]; then
  cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
  echo "Created .env from template"
fi

