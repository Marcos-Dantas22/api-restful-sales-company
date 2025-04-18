from fastapi import FastAPI, Request
from api_restful.routes import auth
from api_restful.routes import clients

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.include_router(auth.router, prefix="/api/v1")
app.include_router(clients.router, prefix="/api/v1")

@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = err['loc'][-1]
        errors.append({
            "field": field,
            "error": err["msg"]
        })
    
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            "message": "Erro de validação nos campos enviados",
            "errors": errors
        }),
    )