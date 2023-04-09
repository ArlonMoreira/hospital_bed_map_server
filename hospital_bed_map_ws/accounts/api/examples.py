from drf_spectacular.utils import OpenApiExample

LOGIN_RESPONSE_EXAMPLES = [
    OpenApiExample(
        "Success",
        description="successfully authenticated user",
        value={
            'message': 'Usuário autenticado com sucesso.',
            'data': [
                {
                    'refresh': 'token_de_atualizacao_sessao',
                    'access': 'seu_token_de_acesso'                           
                }
            ]
        },
        response_only=True,
        status_codes=["200"],
    ),
    OpenApiExample(
        "validation username",
        description="Required username field",
        value={
            'message': 'Campo "username" não especificado.',
            'data': []
        },
        response_only=True,
        status_codes=["400"],
    ),
    OpenApiExample(
        "validation password",
        description="Required password field",
        value={
            'message': 'Campo "password" não especificado.',
            'data': []
        },
        response_only=True,
        status_codes=["400"],
    ),
    OpenApiExample(
        "Failure",
        description="Authentication failed due to incorrect user account or password",
        value={
            'message': 'Certifique-se que o usuário ou senha estão corretos.',
            'data': []
        },
        response_only=True,
        status_codes=["400"],
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