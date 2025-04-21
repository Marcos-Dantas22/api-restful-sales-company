# GET PRODUCTS DOCS

get_products_description = """
### 🛒 Listar Produtos

Este endpoint retorna uma lista de produtos, podendo ser filtrados por categoria, faixa de preço e disponibilidade.

**Regras de negócio:**
- Apenas usuários autenticados podem acessar esta rota.
- Não é permitido utilizar `price` junto com `price_min` ou `price_max` ao mesmo tempo.
- Os resultados são paginados usando os parâmetros `skip` e `limit`.
- O campo availability pode ser 0, para os produtos disponiveis e 1 para os não disponiveis.
"""

get_products_response_example = [
    {
        "id": 1,
        "name": "Camisa Polo",
        "category": "Roupas",
        "price": 79.90,
        "availability": 12
    },
    {
        "id": 2,
        "name": "Tênis Esportivo",
        "category": "Calçados",
        "price": 199.90,
        "availability": 5
    }
]

get_products_responses = {
    200: {
        "description": "Lista de produtos retornada com sucesso.",
        "content": {
            "application/json": {
                "example": get_products_response_example
            }
        }
    },
    400: {
        "description": "Erro de validação nos filtros.",
        "content": {
            "application/json": {
                "example": {
                    "PriceMinFormatoInvalido": {
                        "summary": "Formato inválido em price_min",
                        "value": {
                            "detail": "price_min não pode ser negativo"
                        },
                    },
                    "PriceMaxFormatoInvalido": {
                        "summary": "Formato inválido em price_max",
                        "value": {
                            "detail": "price_max não pode ser negativo"
                        },
                    },
                    "AvabilityFormatoInvalido": {
                        "summary": "Formato inválido em availability",
                        "value": {
                            "detail": "availability deve ser 0 ou 1"
                        },
                    },
                    "FiltersFormatoInvalido": {
                        "summary": "Não permitido multiplos filtros de preço",
                        "value": {
                            "detail": "Não é permitido usar o filtro 'price' junto com 'price_min' ou 'price_max'. Escolha apenas um conjunto de filtros de preço."
                        },
                    },
                }
            }
        }
    },
    401: {
        "description": "Usuário não autenticado.",
        "content": {
            "application/json": {
                "example": {"detail": "Token de autenticação não fornecido"}
            }
        }
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

# POST PRODUCTS DOCS

create_product_description = """
### 📝 Criar Produto

Este endpoint cria um novo produto no sistema.

**Regras de negócio:**
- Apenas usuários autenticados podem acessar esta rota.
- Apenas administradores autenticados podem acessar esta rota.
- O código de barras (barcode) deve ser único, caso contrário, a criação será rejeitada.
- O produto criado retorna uma mensagem de sucesso com os dados do produto.

**Formato do campo 'images':**
As imagens devem ser enviadas como uma lista de strings no formato base64. Exemplo:

```json
"images": [
    "data:image/jpg;base64,..."
]
"""

create_product_request_example = {
    "description": "Camiseta Estampada",
    "section": "Roupas",
    "price": 49.90,
    "initial_stock": 15,
    "barcode": "1234567890123",
    "images": [],
}

create_product_response_example = {
    "id": 1,
    "description": "Camiseta Estampada",
    "section": "Roupas",
    "price": 49.90,
    "initial_stock": 15,
    "barcode": "1234567890123",
    "images": [],
}

create_product_responses = {
    201: {
        "description": "Produto criado com sucesso.",
        "content": {
            "application/json": {
                "example": create_product_response_example
            }
        }
    },
    400: {
        "description": "Erro de validação (Código de barras já está em uso).",
        "content": {
            "application/json": {
                "example": {"detail": "Código de barras já esta sendo utilizado"}
            }
        }
    },
    401: {
        "description": "Usuário não autenticado.",
        "content": {
            "application/json": {
                "example": {"detail": "Token de autenticação não fornecido"}
            }
        }
    },
    403: {
        "description": "Acesso negado. Apenas administradores podem acessar esta rota.",
        "content": {
            "application/json": {
                "example": {"detail": "Acesso permitido apenas para administradores."}
            }
        }
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

# GET PRODUCT DOCS

get_product_description = """
### 📝 Buscar Produto

Este endpoint recupera os dados de um produto específico com base no seu ID.

**Regras de negócio:**
- Apenas usuários autenticados podem acessar esta rota.
- O ID do produto deve ser válido para que os dados sejam encontrados.

**Formato do campo 'images':**
As imagens devem ser enviadas como uma lista de strings no formato base64. Exemplo:

```json
"images": [
    "data:image/jpg;base64,..."
]
"""

get_product_responses = {
    200: {
        "description": "Produto encontrado com sucesso.",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "description": "Produto X",
                    "price": 100.0,
                    "barcode": "123456789",
                    "section": "Alimentos",
                    "initial_stock": 50,
                    "expiration_date": "2025-04-20",
                    "images": [
                        {
                            "id": 1,
                            "base64": "data:image/jpg;base64,..."
                        }
                    ]
                }
            }
        }
    },
    400: {
        "description": "Produto não encontrado.",
        "content": {
            "application/json": {
                "example": {"detail": "Produto não encontrado"}
            }
        }
    },
    401: {
        "description": "Usuário não autenticado.",
        "content": {
            "application/json": {
                "example": {"detail": "Token de autenticação não fornecido"}
            }
        }
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

# PUT PRODUCT DOCS

update_product_description = """
### 📝 Atualizar Produto

Este endpoint atualiza os dados de um produto específico com base no seu ID.

**Regras de negócio:**
- Apenas usuários autenticados podem acessar esta rota.
- Apenas administradores autenticados podem acessar esta rota.
- O produto deve existir no sistema para ser atualizado.
- O código de barras (barcode) deve ser único. Caso já exista outro produto com o mesmo código de barras, a atualização será rejeitada.
- Imagens so serão adicionadas ao produto se foram novas, sem remover as antigas. 
"""

update_product_request_example = {
    "description": "Produto Atualizado",
    "price": 120.0,
    "barcode": "987654321",
    "section": "Eletrodomésticos",
    "initial_stock": 30,
    "expiration_date": "2025-06-15",
    "images": [
        "data:image/jpg;base64,..."
    ]
}

update_product_response_example = {
    "id": 1,
    "description": "Produto Atualizado",
    "price": 120.0,
    "barcode": "987654321",
    "section": "Eletrodomésticos",
    "initial_stock": 30,
    "expiration_date": "2025-06-15",
    "images": [
        {
            "id": 1,
            "url": "data:image/jpg;base64,..."
        }
    ]
}

update_product_responses = {
    200: {
        "description": "Produto atualizado com sucesso.",
        "content": {
            "application/json": {
                "example": update_product_response_example
            }
        }
    },
    400: {
        "description": "Erro de validação (Código de barras já está em uso).",
        "content": {
            "application/json": {
                "example": {"detail": "Codigo de barra já esta sendo utilizado"}
            }
        }
    },
    404: {
        "description": "Produto não encontrado.",
        "content": {
            "application/json": {
                "example": {"detail": "Produto não encontrado"}
            }
        }
    },
    401: {
        "description": "Usuário não autenticado.",
        "content": {
            "application/json": {
                "example": {"detail": "Token de autenticação não fornecido"}
            }
        }
    },
    403: {
        "description": "Acesso negado. Apenas administradores podem acessar esta rota.",
        "content": {
            "application/json": {
                "example": {"detail": "Acesso permitido apenas para administradores."}
            }
        }
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

# DELETE PRODUCT DOCS

delete_product_description = """
### 📝 Deletar Produto

Este endpoint permite deletar um produto específico com base no seu ID.

**Regras de negócio:**
- Apenas usuários autenticados podem acessar esta rota.
- Apenas administradores autenticados podem acessar esta rota.
- O produto deve existir no sistema para ser deletado.

Após a exclusão, o produto é removido permanentemente do sistema e não pode ser recuperado.
"""

delete_product_responses = {
    200: {
        "description": "Produto deletado com sucesso.",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "description": "Produto Excluído",
                    "price": 100.0,
                    "barcode": "123456789",
                    "section": "Eletrodomésticos",
                    "initial_stock": 50,
                    "expiration_date": "2025-01-01",
                    "images": [
                        {
                            "id": 1,
                            "url": "data:image/jpg;base64,..."
                        }
                    ]
                }
            }
        }
    },
    401: {
        "description": "Usuário não autenticado.",
        "content": {
            "application/json": {
                "example": {"detail": "Token de autenticação não fornecido"}
            }
        }
    },
    403: {
        "description": "Acesso negado. Apenas administradores podem acessar esta rota.",
        "content": {
            "application/json": {
                "example": {"detail": "Acesso permitido apenas para administradores."}
            }
        }
    },
    404: {
        "description": "Produto não encontrado.",
        "content": {
            "application/json": {
                "example": {"detail": "Produto não encontrado"}
            }
        }
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

# GET PRODUCT HISTORY DOCS

get_product_history_description = """
### 📚 Histórico de Produto

Este endpoint retorna todos os registros de alterações feitas em um produto específico com base no seu ID.

**Informações retornadas por item:**
- `id`: Identificador único do histórico
- `product_id`: ID do produto (pode ser `null` se o produto foi deletado)
- `user_id`: ID do usuário que realizou a ação
- `action`: Tipo da ação (`update` ou `delete`)
- `changed_fields`: Dicionário com os campos alterados e seus valores antigos e novos
- `timestamp`: Data e hora da alteração

**Regras de negócio:**
- Apenas usuários autenticados podem acessar esta rota.
- Apenas administradores autenticados podem acessar esta rota.
- O produto deve existir no sistema para que haja histórico.
"""

get_product_history_responses = {
    200: {
        "description": "Histórico retornado com sucesso.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": 1,
                        "product_id": 42,
                        "user_id": 3,
                        "action": "update",
                        "changed_fields": {
                            "price": {"old_value": 12.33, "new_value": 13.50},
                            "description": {"old_value": "Lasanha", "new_value": "Lasanha Vegana"}
                        },
                        "timestamp": "2025-04-21T12:34:56.789000"
                    },
                    {
                        "id": 2,
                        "product_id": None,
                        "user_id": 3,
                        "action": "delete",
                        "changed_fields": {
                            "id": 42,
                            "description": "Lasanha Vegana",
                            "price": 13.50,
                            "barcode": "777777777",
                            "section": "Congelados",
                            "initial_stock": 50,
                            "expiration_date": "2025-04-21"
                        },
                        "timestamp": "2025-04-21T12:40:00.123000"
                    }
                ]
            }
        }
    },
    401: {
        "description": "Usuário não autenticado.",
        "content": {
            "application/json": {
                "example": {"detail": "Token de autenticação não fornecido"}
            }
        }
    },
    403: {
        "description": "Acesso negado. Apenas administradores podem acessar esta rota.",
        "content": {
            "application/json": {
                "example": {"detail": "Acesso permitido apenas para administradores."}
            }
        }
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
