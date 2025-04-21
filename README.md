# 🚀 API RESTful - Sales Company

Uma poderosa e elegante API RESTful desenvolvida com **FastAPI**, seguindo as melhores práticas de segurança, testes, versionamento e deploy com Docker. Ideal para aplicações escaláveis e modernas.

---

## 🛠️ Tecnologias Utilizadas

- **[Python 3.11](https://www.python.org/)**
- **[FastAPI](https://fastapi.tiangolo.com/)** – Web framework rápido e moderno
- **[PostgreSQL](https://www.postgresql.org/)** – Banco de dados relacional
- **[Docker](https://www.docker.com/)** – Containerização da aplicação
- **[SQLAlchemy](https://www.sqlalchemy.org/)** – ORM para modelagem do banco
- **[Alembic](https://alembic.sqlalchemy.org/)** – Migrações de banco de dados
- **[Pytest](https://docs.pytest.org/)** – Testes automatizados
- **[Pydantic](https://docs.pydantic.dev/)** – Validação de dados com Python
- **[JWT - python-jose](https://github.com/mpdavis/python-jose)** – Autenticação segura via tokens
- **[Passlib](https://passlib.readthedocs.io/)** – Criptografia de senhas
- **[Sentry](https://sentry.io/)** – Monitoramento de erros em tempo real

---

## 📦 Como rodar o projeto com Docker

```bash
# Clone o projeto
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio

# Crie o arquivo .env com as variáveis de ambiente necessárias
cp .env.example .env

# Suba a aplicação com Docker Compose
docker-compose up --build