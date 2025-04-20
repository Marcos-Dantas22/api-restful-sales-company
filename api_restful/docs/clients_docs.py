# GET CLIENTS DOCS

get_clients_description = """
### 📋 Listar Clientes

Este endpoint permite listar os clientes cadastrados no sistema com suporte a filtros e paginação.

**Regras de negócio:**
- Apenas usuários autenticados podem acessar esta rota.
- Os filtros por nome completo e e-mail são opcionais.
- A resposta é paginada, com parâmetros `skip` e `limit`.

"""

get_clients_success_response = [
      {
        "id": 5,
        "full_name": "Ana Beatriz",
        "cpf": "200.111.222-33",
        "gender": "Feminino",
        "email": "ana.beatriz@example.com",
        "phone": "(86) 98223-3993",
        "birth_date": "1995-06-15",
        "address": "Av. Central, 456",
        "city": "Imperatriz",
        "state": "MA"
    },
    {
        "id": 2,
        "full_name": "Maria Souza",
        "cpf": "200.111.222-33",
        "gender": "Feminino",
        "email": "maria@email.com",
        "phone": "(98) 98119-3993",
        "birth_date": "1995-06-15",
        "address": "Av. Central, 456",
        "city": "Imperatriz",
        "state": "MA"
    }
]

get_clients_responses = {
    200: {
        "description": "Lista de clientes retornada com sucesso.",
       "content": {
            "application/json": {
                "examples": {
                    "com_clientes": {
                        "summary": "Lista com clientes",
                        "value": get_clients_success_response
                    },
                    "sem_clientes": {
                        "summary": "Lista vazia",
                        "value": []
                    }
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

# POST CLIENTS DOCS

create_client_description = """
### 📝 Criar Cliente

Este endpoint permite criar um novo cliente no sistema. O cliente será associado ao usuário autenticado e será verificado a duplicidade de CPF e e-mail antes da criação.

**Regras de negócio:**
- Apenas usuários autenticados podem acessar esta rota.
- O CPF e o e-mail devem ser exclusivos no sistema, caso contrário, a criação será rejeitada.
- A criação do cliente retorna uma mensagem de sucesso e os dados do cliente criado.
  
"""

create_client_request_example = {
    "full_name": "Maria Souza",
    "cpf": "200.111.222-33",
    "gender": "female",
    "email": "maria@email.com",
    "phone": "(98) 98119-3993",
    "birth_date": "1995-06-15",
    "address": "Av. Central, 456",
    "city": "Imperatriz",
    "state": "MA"
}

create_client_response_example = {
    "id": 4,
    "full_name": "Maria Souza",
    "cpf": "200.111.222-33",
    "gender": "Feminino",
    "email": "maria@email.com",
    "phone": "(98) 98119-3993",
    "birth_date": "1995-06-15",
    "address": "Av. Central, 456",
    "city": "Imperatriz",
    "state": "MA"
}

create_client_responses = {
    201: {
        "description": "Cliente criado com sucesso.",
        "content": {
            "application/json": {
                "example": create_client_response_example
            }
        }
    },
    400: {
        "description": "Erro de validação (CPF ou e-mail já estão em uso).",
        "content": {
            "application/json": {
                "examples": {
                    "cpf_ja_em_uso": {
                        "summary": "CPF já está em uso",
                        "value": {"detail": "CPF já está em uso"}
                    },
                    "email_ja_em_uso": {
                        "summary": "Email já está em uso",
                        "value": {"detail": "Email já está em uso"}
                    }
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

# GET CLIENT DOCS

get_client_description = """
### 🔍 Buscar Cliente por ID

Este endpoint recupera os dados de um cliente específico com base no seu ID.

**Regras de negócio:**
- Apenas usuários autenticados podem acessar esta rota.
- Caso o cliente não seja encontrado, uma mensagem de erro será retornada.
- A resposta trará os dados completos do cliente, incluindo informações de contato e localização.
"""

get_client_response_example = {
    "id": 8,
    "full_name": "Jorge Silva",
    "cpf": "123.456.789-00",
    "gender": "Masculino",
    "email": "jorge@example.com",
    "phone": "(98) 98123-4567",
    "birth_date": "1990-05-15",
    "address": "Rua das Flores, 123",
    "city": "São Luís",
    "state": "MA"
}

get_client_responses = {
    200: {
        "description": "Cliente encontrado com sucesso.",
        "content": {
            "application/json": {
                "example": get_client_response_example
            }
        }
    },
    400: {
        "description": "Cliente não encontrado.",
        "content": {
            "application/json": {
                "example": {"detail": "Cliente não encontrado"}
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

# PUT CLIENT DOCS

update_client_description = """
### 🔄 Atualizar Cliente

Este endpoint permite atualizar os dados de um cliente já existente, informando o ID do cliente e os novos dados.

**Regras de negócio:**
- Apenas usuários autenticados podem acessar esta rota.
- O CPF e o e-mail devem ser únicos no sistema. Se já estiverem em uso por outro cliente, a atualização será rejeitada.
- Caso o cliente com o ID fornecido não exista, será retornado um erro.
- A resposta trará os dados atualizados do cliente.
"""

update_client_request_example = {
    "full_name": "Joana Costa",
    "cpf": "987.654.321-00",
    "gender": "female",
    "email": "joana@example.com",
    "phone": "(98) 99123-4567",
    "birth_date": "1988-11-23",
    "address": "Rua Nova, 789",
    "city": "Bacabal",
    "state": "MA"
}

update_client_response_example = {
    "id": 2,
    "full_name": "Joana Costa",
    "cpf": "987.654.321-00",
    "gender": "Feminino",
    "email": "joana@example.com",
    "phone": "(98) 99123-4567",
    "birth_date": "1988-11-23",
    "address": "Rua Nova, 789",
    "city": "Bacabal",
    "state": "MA"
}

update_client_responses = {
    200: {
        "description": "Cliente atualizado com sucesso.",
        "content": {
            "application/json": {
                "example": update_client_response_example
            }
        }
    },
    400: {
        "description": "Erro de validação (CPF ou e-mail já estão em uso).",
        "content": {
            "application/json": {
                "examples": {
                    "cpf_ja_em_uso": {
                        "summary": "CPF já está em uso",
                        "value": {"detail": "CPF já está em uso"}
                    },
                    "email_ja_em_uso": {
                        "summary": "Email já está em uso",
                        "value": {"detail": "Email já está em uso"}
                    }
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
    404: {
        "description": "Cliente não encontrado.",
        "content": {
            "application/json": {
                "example": {"detail": "Cliente não encontrado"}
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

# DELETE CLIENT DOCS

delete_client_description = """
### ❌ Deletar Cliente

Este endpoint exclui permanentemente um cliente do sistema com base no seu ID.

**Regras de negócio:**
- Apenas usuários autenticados podem acessar esta rota.
- Caso o cliente com o ID fornecido não exista, será retornado um erro.
- O retorno trará os dados do cliente que foi excluído.
"""

delete_client_response_example = {
    "id": 3,
    "full_name": "Carlos Mendes",
    "cpf": "111.222.333-44",
    "gender": "Masculino",
    "email": "carlos@example.com",
    "phone": "(98) 98123-1234",
    "birth_date": "1990-03-12",
    "address": "Rua das Flores, 100",
    "city": "São Luís",
    "state": "MA"
}

delete_client_responses = {
    200: {
        "description": "Cliente deletado com sucesso.",
        "content": {
            "application/json": {
                "example": delete_client_response_example
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
    404: {
        "description": "Cliente não encontrado.",
        "content": {
            "application/json": {
                "example": {"detail": "Cliente não encontrado"}
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