from drf_spectacular.utils import OpenApiExample

REFRESH_TOKEN_RESPONSE_EXAMPLES = [
    OpenApiExample(
        "Success",
        description='<p>Quando autenticado com sucesso a sessão é renovada, sendo retornado o refresh token que foi utilizado na requisição e o novo access token.</p>\
        <i>When the session is successfully authenticated, the refresh token that was informed in the request and the new access token are returned.</i>',
        value={
            'message': 'Sessão renovada.',
            'data': {
                'refresh': 'token_de_atualizacao_sessao',
                'access': 'seu_token_de_acesso'                           
            }
        },
        response_only=True,
        status_codes=["200"],        
    ),
    OpenApiExample(
        "Access Denied",
        description='<p>Quando o token de atualização refresh é inválido ou expirou ocorre falha de autenticação.</p>\
        <i>When the refresh refresh token is invalid or expired, authentication fails.</i>',
        value={
            'message': 'Sua sessão foi encerrada.',
            'data': {
                'refresh': [
                    'Token inválido.',
                    'Este campo é obrigatório.'
                ],                         
            }
        },
        response_only=True,
        status_codes=["401"],        
    ),    
]

REFRESH_TOKEN_REQUEST = {
    "application/json": {
        "type": "object",
        "properties": {
            "refresh": {"type": "string", "description": "Refresh token", "required": True},
        }
    },    
}

LOGIN_RESPONSE_EXAMPLES = [
    OpenApiExample(
        "Success",
        description='<p>Quando a autenticação ocorre com sucesso, é retornado dois tokens, "access" para realizar autenticação e "refresh" para atualizar o token "access".</p>\
        <i>When authentication is successful, two tokens are returned, "access" to perform authentication and "refresh" to update the "access" token.</i>',
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
        "Access Denied",
        description='<p>Um erro ocorre quando as credenciais de autenticação não foram informadas corretamente ou não satisfaz a condição para que o usuário seja autenticado.</p>\
        <i>An error occurs when the authentication credentials were not authenticated correctly or were not the condition for the user to be authenticated.</i>',
        value={
            "message": "Acesso negado por falha de autenticação",
            "data": {
                "username": [
                    "Usuário não cadastrado.",
                    "Este campo não pode ser em branco.",
                    "Este campo é obrigatório."
                ],
                "password": [
                    "Este campo é obrigatório.",
                    "Este campo não pode ser em branco.",
                    "Senha incorreta."
                ]                
            }
        },
        response_only=True,
        status_codes=["401"],
    )      
]

LOGIN_REQUESTS = {
    "application/json": {
        "type": "object",
        "properties": {
            "username": {"type": "string", "description": "Username", "required": True},
            "password": {"type": "string", "description": "Password", "format": "password", "required": True},
        }
    },
    "multipart/form-data": {
        "type": "object",
        "properties": {
            "username": {"type": "string", "description": "Username", "required": True},
            "password": {"type": "string", "description": "Password", "format": "password", "required": True},
        }
    },      
}