from drf_spectacular.utils import OpenApiExample

LOGIN_RESPONSE_EXAMPLES = [
    OpenApiExample(
        "Success",
        description="successfully authenticated user",
        value={
            'message': 'Usuário autenticado com sucesso.',
            'data': {
                'refresh': 'token_de_atualizacao_sessao',
                'access': 'seu_token_de_acesso'                           
            }
        },
        response_only=True,
        status_codes=["200"],
    ),
    OpenApiExample(
        "validations field username",
        description="validations username",
        value={
            "message": "Certifique-se que o usuário ou senha estão corretos.",
            "data": {
                "username": [
                    "Usuário não cadastrado.",
                    "Este campo não pode ser em branco.",
                    "Este campo é obrigatório."
                ]
            }
        },
        response_only=True,
        status_codes=["401"],
    ),
    OpenApiExample(
        "validations field password",
        description="validations password",
        value={
            "message": "Certifique-se que o usuário ou senha estão corretos.",
            "data": {
                "password": [
                    "Este campo é obrigatório.",
                    "Este campo não pode ser em branco."
                ]
            }
        },
        response_only=True,
        status_codes=["401"],
    ),
    OpenApiExample(
        "Failure",
        description="Authentication failed due to incorrect user account or password",
        value={
            'message': 'Certifique-se que o usuário ou senha estão corretos.',
            'data': {}
        },
        response_only=True,
        status_codes=["401"],
    ),        
]

LOGIN_REQUESTS = {
    "application/json": {
        "type": "object",
        "properties": {
            "username": {"type": "string", "description": "Username"},
            "password": {"type": "string", "description": "Password", "format": "password"},
        }
    },
    "multipart/form-data": {
        "type": "object",
        "properties": {
            "username": {"type": "string", "description": "Username"},
            "password": {"type": "string", "description": "Password", "format": "password"},
        }
    },      
}