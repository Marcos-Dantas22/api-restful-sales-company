# LOGIN DOCS

login_description = """
### 🔐 Login de usuário

Este endpoint realiza o login do usuário no sistema.

- O usuário deve estar previamente cadastrado no banco de dados.
- A senha deve ser válida e será verificada.
- Será retornado um token JWT em caso de sucesso.

"""

login_request_example = {
    "username": "admin",
    "password": "123456"
}

login_success_response = {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}

login_responses = {
    200: {
        "description": "Login realizado com sucesso.",
        "content": {
            "application/json": {
                "example": login_success_response
            }
        },
    },
   404: {
        "description": "Usuário não encontrado ou senha incorreta.",
        "content": {
            "application/json": {
                "examples": {
                    "usuario_nao_encontrado": {
                        "summary": "Usuário não encontrado",
                        "value": {"detail": "Usuário não encontrado"}
                    },
                    "senha_incorreta": {
                        "summary": "Senha incorreta",
                        "value": {"detail": "Senha incorreta"}
                    }
                }
            }
        },
    },
    422: {
        "description": "Erro de validação nos campos enviados.",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de validação nos campos enviados",
                    "errors": [
                        {
                            "field": "campo",
                            "error": "mensagem de erro"
                        }
                    ]
                }
            }
        }
    }
    
}

# REGISTER USER DOCS

register_description = """
### 🧾 Registro de novo usuário

Este endpoint permite que um novo usuário seja criado no sistema.

- O nome de usuário deve ser único.
- A senha deve ser enviada corretamente.
- O usuário será salvo no banco de dados com uma senha criptografada.

"""

register_request_example = {
    "username": "novousuario",
    "password": "senhaSegura123"
}

register_success_response = {
    "message": "Usuario criado com sucesso",
    "system_user_id": 1
}

register_responses = {
    200: {
        "description": "Usuário criado com sucesso.",
        "content": {
            "application/json": {
                "example": register_success_response
            }
        },
    },
    400: {
        "description": "Username já cadastrado.",
        "content": {
            "application/json": {
                "example": {"detail": "Username já cadastrado"}
            }
        },
    },
    422: {
        "description": "Erro de validação nos campos enviados.",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de validação nos campos enviados",
                    "errors": [
                        {
                            "field": "campo",
                            "error": "mensagem de erro"
                        }
                    ]
                }
            }
        }
    }
}

# REFRESH TOKEN DOCS

refresh_token_description = """
### 🔄 Refresh de Token JWT

Este endpoint gera um novo token de acesso com base em um refresh token válido.

**Regras de negócio:**
- O refresh token deve ser válido e não expirado.
- O token deve conter o campo `sub` com o nome de usuário.
- Um novo token JWT será gerado se o refresh token for válido.

"""

refresh_token_request_example = {
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

refresh_token_success_response = {
    "message": "Novo token gerado com sucesso",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

refresh_token_responses = {
    200: {
        "description": "Novo token gerado com sucesso.",
        "content": {
            "application/json": {
                "example": refresh_token_success_response
            }
        },
    },
    401: {
        "description": "Token inválido ou expirado.",
        "content": {
            "application/json": {
                "example": {"detail": "Refresh token inválido ou expirado"}
            }
        },
    },
    422: {
        "description": "Erro de validação nos campos enviados.",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de validação nos campos enviados",
                    "errors": [
                        {
                            "field": "campo",
                            "error": "mensagem de erro"
                        }
                    ]
                }
            }
        }
    }
}

# REGISTER USER ADMIN DOCS

register_admin_description = """
### 👑 Registrar Usuário Admin

Este endpoint permite que um **usuário autenticado com permissão de administrador** registre um novo usuário administrador no sistema.

**Regras de acesso:**
- Apenas administradores autenticados (`is_admin: true`) podem acessar esta rota.
- O `username` informado não pode estar cadastrado previamente.

**Campos obrigatórios:**
- `username`: Nome de usuário único
- `password`: Senha do novo administrador
"""

register_admin_responses = {
    200: {
        "description": "Usuário administrador criado com sucesso.",
        "content": {
            "application/json": {
                "example": {
                    "message": "Usuario Admin criado com sucesso",
                    "system_user_id": 42
                }
            }
        }
    },
    400: {
        "description": "Username já cadastrado.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Username já cadastrado"
                }
            }
        }
    },
    403: {
        "description": "Acesso negado. Usuário não é administrador.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Acesso permitido apenas para administradores."
                }
            }
        }
    },
    422: {
        "description": "Erro de validação nos dados enviados.",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de validação nos campos enviados",
                    "errors": [
                        {
                            "field": "username",
                            "error": "campo obrigatório"
                        },
                        {
                            "field": "password",
                            "error": "campo obrigatório"
                        }
                    ]
                }
            }
        }
    }
}
