#!/bin/bash
# start.sh

echo "▶ Rodando as migrations..."
alembic upgrade head

echo "👤 Criando usuário admin padrão..."
python -m api_restful.utils.create_admin_user

echo "🚀 Iniciando servidor FastAPI..."
exec uvicorn api_restful.main:app --host 0.0.0.0 --port 8000