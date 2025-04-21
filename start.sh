#!/bin/bash
# start.sh

echo "▶ Rodando as migrations..."
alembic upgrade head

echo "🚀 Iniciando servidor FastAPI..."
exec uvicorn api_restful.main:app --host 0.0.0.0 --port 8000