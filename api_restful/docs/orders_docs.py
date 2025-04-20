# GET ORDERS DOCS

get_orders_description = """
### 📝 Obter Pedidos

Este endpoint permite obter uma lista de pedidos, com a possibilidade de aplicar filtros como data, seção, status, ID do cliente, etc. Os resultados podem ser paginados utilizando os parâmetros `skip` e `limit`.

**Parâmetros de Filtro:**
- **start_date** (opcional): Data de início para filtrar os pedidos, exemplo: 2025-04-19.
- **end_date** (opcional): Data de término para filtrar os pedidos, exemplo: 2025-04-19.
- **section** (opcional): Seção para filtrar os pedidos.
- **order_id** (opcional): ID do pedido para buscar um pedido específico.
- **status** (opcional): Status do pedido.
- **client_id** (opcional): ID do cliente para filtrar os pedidos de um cliente específico.
- **skip** (opcional): Pular um número específico de pedidos para paginação.
- **limit** (opcional): Limitar o número de pedidos retornados, com valor mínimo de 1 e máximo de 1000.

**Regras de negócio:**
- Somente usuários autenticados podem acessar esta rota.
- Os pedidos são filtrados de acordo com os parâmetros fornecidos e são retornados com base nas condições especificadas.
"""

get_orders_responses = {
    200: {
        "description": "Lista de pedidos recuperada com sucesso.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": 1,
                        "order_date": "2025-03-10T10:00:00",
                        "status": "Em andamento",
                        "client_id": 123,
                        "total_amount": 200.0,
                        "items": [
                            {
                                "product_id": 456,
                                "quantity": 2,
                                "price": 100.0
                            }
                        ]
                    },
                    {
                        "id": 2,
                        "order_date": "2025-03-11T11:00:00",
                        "status": "Concluído",
                        "client_id": 124,
                        "total_amount": 300.0,
                        "items": [
                            {
                                "product_id": 457,
                                "quantity": 3,
                                "price": 100.0
                            }
                        ]
                    }
                ]
            }
        }
    },
   400: {
        "description": "Erro de validação de filtros de busca",
        "content": {
            "application/json": {
                "examples": {
                    "StartDateFormatoInvalido": {
                        "summary": "Formato inválido em start_date",
                        "value": {
                            "detail": "start_date deve estar no formato YYYY-MM-DD"
                        },
                    },
                    "EndDateFormatoInvalido": {
                        "summary": "Formato inválido em end_date",
                        "value": {
                            "detail": "end_date deve estar no formato YYYY-MM-DD"
                        },
                    },
                    "SectionVazia": {
                        "summary": "Section está vazia",
                        "value": {
                            "detail": "section não pode ser uma string vazia"
                        },
                    },
                    "StatusInvalido": {
                        "summary": "Status não permitido",
                        "value": {
                            "detail": "status inválido. Valores permitidos: created, processing, completed, canceled"
                        },
                    },
                    "OrderIdInvalido": {
                        "summary": "order_id menor que 1",
                        "value": {
                            "detail": "order_id deve ser maior que 0"
                        },
                    },
                    "ClientIdInvalido": {
                        "summary": "client_id menor que 1",
                        "value": {
                            "detail": "client_id deve ser maior que 0"
                        },
                    },
                }
            }
        },
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

# CREATE ORDERS DOC

create_orders_description = """
📝 Cria um novo pedido na plataforma.

- Verifica se o cliente existe.
- Valida os produtos enviados, conferindo estoque.
- Lança erro se algum produto estiver em falta ou não for encontrado.
"""

create_orders_responses = {
    400: {
        "description": "Erro de validação ao criar pedido",
        "content": {
            "application/json": {
                "examples": {
                    "ClienteNaoEncontrado": {
                        "summary": "Cliente não encontrado",
                        "value": {
                            "detail": "Cliente não encontrado"
                        },
                    },
                }
            }
        },
    },
    404: {
        "description": "Produto não encontrado ou sem estoque",
        "content": {
            "application/json": {
                "examples": {
                    "ProdutoNaoEncontrado": {
                        "summary": "Produto inexistente",
                        "value": {
                            "detail": "Produto não encontrado."
                        },
                    },
                    "EstoqueInsuficiente": {
                        "summary": "Estoque abaixo do necessário",
                        "value": {
                            "detail": "Estoque insuficiente para o produto 'Produto A'. Quantidade solicitada: 10, disponível: 5."
                        },
                    },
                }
            }
        },
    },
    401: {
        "description": "Usuário não autenticado.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Token de autenticação não fornecido"
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

# GET ORDER BY ID DOC

get_order_description = """
📦 Retorna os detalhes de um pedido específico.

- Busca o pedido pelo ID.
- Retorna erro caso o pedido não seja encontrado.
"""

get_order_responses = {
    400: {
        "description": "Pedido não encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Pedido não encontrado"
                }
            }
        },
    },
    401: {
        "description": "Usuário não autenticado.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Token de autenticação não fornecido"
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

# UPDATE ORDER DOC

update_orders_description = """
✏️ Atualiza as informações de um pedido existente.

- Busca o pedido pelo ID.
- Atualiza os campos fornecidos no corpo da requisição.
- Retorna erro se o pedido não for encontrado.
- produtos so serão adicionados ao pedido se forem novos, sem remover os antigas. 
- e possivel alterar a quantidade de um pedido, setando o id do produto e um novo valor de quantity
"""

update_orders_responses = {
    200: {
        "description": "Pedido atualizado com sucesso",
    },
    404: {
        "description": "Pedido não encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Pedido não encontrado"
                }
            }
        },
    },
    401: {
        "description": "Usuário não autenticado.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Token de autenticação não fornecido"
                }
            }
        },
    },
    422: {
        "description": "Erro de validação nos dados enviados.",
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
        },
    },
}

# DELETE ORDER DOC

delete_order_description = """
🗑️ Deleta um pedido existente na plataforma.

- Busca o pedido pelo ID e o deleta.
- Retorna erro se o pedido não for encontrado.
"""

delete_order_responses = {
    200: {
        "description": "Pedido deletado com sucesso",
    },
    404: {
        "description": "Pedido não encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Pedido não encontrado"
                }
            }
        },
    },
    401: {
        "description": "Usuário não autenticado.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Token de autenticação não fornecido"
                }
            }
        },
    },
    422: {
        "description": "Erro de validação nos dados enviados.",
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
        },
    },
}