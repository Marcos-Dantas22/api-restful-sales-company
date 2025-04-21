from fastapi import FastAPI, Request
from api_restful.routes import auth
from api_restful.routes import clients
from api_restful.routes import products
from api_restful.routes import orders
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

tags_metadata = [
    {
        "name": "Autenticação",
        "description": "Operações relacionadas ao login e token.",
    },
    {
        "name": "Clientes",
        "description": "Gerenciamento dos clientes cadastrados, incluindo criação, consulta e remoção.",
    },
    {
        "name": "Produtos",
        "description": "Controle de produtos em estoque, incluindo cadastro, consulta e exclusão.",
    },
    {
        "name": "Pedidos",
        "description": "Gerenciamento dos pedidos realizados, incluindo criação, acompanhamento e histórico.",
    },
]

sentry_sdk.init(
    dsn="https://0b77df24223fc77ee826bcf912a4c849@o4509192557494272.ingest.us.sentry.io/4509192559329280",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    environment="production",
)

app = FastAPI(
    title="API-RESTFUL Sistema de Vendas",
    description="API responsável pelo gerenciamento de vendas, controle de estoque, registro de pedidos e administração de clientes.",
    version="1.0.0",
    contact={
        "name": "Marcos Vinícius",
        "email": "marcosdantaslkdin@gmail.com"
    },
    docs_url="/docs", 
    redoc_url="/redoc",
    servers=[
        {"url": "http://localhost:8000/", "description": "Local Dev"},
        {"url": "https://api-restful-sales-company-40wp.onrender.com/", "description": "Produção"}
    ],
    openapi_tags=tags_metadata  
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(clients.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")

app.add_middleware(SentryAsgiMiddleware)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://api-restful-sales-company-40wp.onrender.com/"],  
    allow_credentials=True,
    allow_methods=["https://api-restful-sales-company-40wp.onrender.com/"],
    allow_headers=["https://api-restful-sales-company-40wp.onrender.com/"],
)

# @app.get("/sentry-debug")
# async def trigger_error():
#     division_by_zero = 1 / 0

@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = err['loc'][-1]
        message = traduction(err["msg"])

        errors.append({
            "field": field,
            "error": message,
        })
    
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            "message": "Erro de validação nos campos enviados",
            "errors": errors
        }),
    )

def traduction(msg: str) -> str:
    # Remove o prefixo automático do Pydantic
    if msg.startswith("Value error, "):
        msg = msg.replace("Value error, ", "", 1)

    traducoes = {
        "Field required": "Campo obrigatório",
        "Input should be a valid string": "O valor deve ser uma string válida",
        "Value is not a valid integer": "O valor não é um número inteiro válido",
        "Input should be a valid email address": "O valor deve ser um e-mail válido",
        "Ensure this value has at least 1 characters": "O valor deve ter pelo menos 1 caractere",
        "Input should be 'female', 'male' or 'other'": "O valor deve ser 'female, 'male' ou 'other'",
        "value is not a valid email address: An email address must have an @-sign.": "O valor deve ser um e-mail válido",
        "Input should be a valid number, unable to parse string as a number": "O valor deve ser um número válido",
        "Input should be a valid integer, unable to parse string as an integer": "O valor deve ser um número inteiro válido",
    }
    return traducoes.get(msg, msg)  