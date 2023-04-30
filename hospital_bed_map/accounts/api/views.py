from django.contrib.auth import authenticate, login, logout
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_spectacular.utils import extend_schema, OpenApiTypes
from .serializer import LoginSerializer
from ..utils import get_tokens_for_user
from .examples import LOGIN_RESPONSE_EXAMPLES, LOGIN_REQUESTS, REFRESH_TOKEN_RESPONSE_EXAMPLES, REFRESH_TOKEN_REQUEST

#Customiza a atualização do token para retornar também o refresh token como resposta
class RefreshTokenView(TokenRefreshView, mixins.ListModelMixin, mixins.CreateModelMixin):

    def handle_exception(self, exc):
        if isinstance(exc, InvalidToken) or isinstance(exc, TokenError):
            return Response({'message': 'Sua sessão foi encerrada.', 'data': {"refresh": ['Token inválido.']}}, status=status.HTTP_401_UNAUTHORIZED)
        return super().handle_exception(exc)    

    @extend_schema(
        description='<p>Esse endpoint é responsável por renovar o token de autenticação do usuário. O endpoint recebe o token atual do usuário em uma solicitação POST e, se o token for válido, o servidor gerará um novo token de acesso. O novo token substitui o token antigo e é válido por um período específico. Esse endpoint permite que os usuários mantenham a sessão ativa na aplicação, evitando que precisem fazer login novamente após um certo tempo. Esse endpoint usa o método POST e requer que o usuário esteja autenticado com um token de acesso válido.</p>\
        <i>This endpoint is responsible for renewing the users authentication token. The endpoint receives the users current token in a POST request, and if the token is valid, the server generates a new access token. The new token replaces the old token and is valid for a specific period. This endpoint allows users to keep the session active in the application, avoiding the need to log in again after a certain time. This endpoint uses the POST method and requires the user to be authenticated with a valid access token.</i>',
        auth=False,
        responses={
            200: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT
        },
        examples=REFRESH_TOKEN_RESPONSE_EXAMPLES,
        request=REFRESH_TOKEN_REQUEST
    )    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not(serializer.is_valid()):
            return Response({'message': 'Sua sessão foi encerrada.', 'data': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh_token = serializer.validated_data.get('refresh')
        refresh = RefreshToken(refresh_token)
        data = {
            'message': 'Sessão renovada.',
            'data': {
                'refresh': request.data['refresh'],
                'access': str(refresh.access_token),      
            }
        }

        return Response(data)

#Class responsible for performing user authentication via REST API
class LoginView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    @extend_schema(
        description='<p>O endpoint de autenticação Login é responsável por permitir que um usuário se autentique na aplicação. O endpoint recebe as credenciais do usuário (nome de usuário e senha) em uma requisição POST e realiza a validação dessas informações utilizando a classe LoginSerializer. Se as credenciais forem válidas, a classe realiza o login do usuário e retorna um token de autenticação na resposta da requisição. Esse token é necessário para que o usuário possa acessar as funcionalidades da aplicação que requerem autenticação. Se as credenciais não forem válidas, a classe retorna uma mensagem de erro informando que o usuário ou a senha estão incorretos. Este endpoint utiliza o método POST e não requer autenticação.</p> \
        <i>The Login endpoint is responsible for allowing a user to authenticate in the application. The endpoint receives the user credentials (username and password) in a POST request and validates them using the LoginSerializer class. If the credentials are valid, the class logs the user in and returns an authentication token in the response of the request. This token is necessary for the user to access the application features that require authentication. If the credentials are invalid, the class returns an error message indicating that the username or password is incorrect. This endpoint uses the POST method and does not require authentication. This description will be used in the extend_schema marker for documentation in the OpenAPI format.</i>',
        auth=False,
        responses={
            200: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT
        },
        examples=LOGIN_RESPONSE_EXAMPLES,
        request=LOGIN_REQUESTS
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not(serializer.is_valid()):
            return Response({'message': 'Acesso negado por falha de autenticação.', 'data': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = serializer.data

        '''
        #https://docs.djangoproject.com/en/4.1/topics/auth/default/
        authenticate() method checks if the authentication credentials are valid. returns a User object if
        the credentials are valid for a backend. If credentials are not valid for any backend
        or if a backend throws PermissionDe
        '''        
        user = authenticate(request, username=serializer['username'], password=serializer['password'])
        if user is not None:
            '''
            The login() method logs in and saves the user ID to the session, using Django's session framework.
            '''
            login(request, user)
            data = get_tokens_for_user(user)

            return Response({'message': 'Usuário autenticado com sucesso.', 'data': data}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Acesso negado por falha de autenticação.', 'data': {
            'password': [
                'Senha incorreta.'
            ]
        }}, status=status.HTTP_401_UNAUTHORIZED)
