#!/bin/bash

echo "🔧 Gerando arquivo .env..."

cat <<EOF > .env
# Banco principal
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=database
DATABASE_URL=postgresql://postgres:postgres@db:5432/database

# Banco de testes
POSTGRES_TEST_USER=test_user
POSTGRES_TEST_PASSWORD=test_user12345
POSTGRES_TEST_DB=test_database
TEST_DATABASE_URL=postgresql://test_user:test_user12345@test_db:5432/test_database

# Segurança
SECRET_KEY=K9tv4D2pLEOZ5JdknS4OEK0_PpTxF3NyVfWyMtK6Ngk
EOF

echo "✅ Arquivo .env criado com sucesso!"
