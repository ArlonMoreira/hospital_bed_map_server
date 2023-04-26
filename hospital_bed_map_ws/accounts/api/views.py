from django.contrib.auth import authenticate, login, logout
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiExample
from .serializer import LoginSerializer
from ..utils import get_tokens_for_user
from .examples import LOGIN_RESPONSE_EXAMPLES, LOGIN_REQUESTS

#Customiza a atualização do token para retornar também o refresh token como resposta
class RefreshTokenView(TokenRefreshView):

    def handle_exception(self, exc):
        if isinstance(exc, InvalidToken) or isinstance(exc, TokenError):
            return Response({'message': 'Sua sessão foi encerrada.', 'data': {}}, status=status.HTTP_401_UNAUTHORIZED)
        return super().handle_exception(exc)    

    @extend_schema(
        description='Refresh access token.',
        auth=False,
        responses={
            200: OpenApiTypes.OBJECT
        },
        examples=LOGIN_RESPONSE_EXAMPLES
    )    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
        description='Perform user login.',
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
            return Response({'message': 'Certifique-se que o usuário ou senha estão corretos.', 'data': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
        
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
        
        return Response({'message': 'Certifique-se que o usuário ou senha estão corretos.', 'data': {}}, status=status.HTTP_401_UNAUTHORIZED)

#Class responsible for terminating the session
class LogoutView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        description='Terminate the user session.',
        auth=False,
        responses={
            200: OpenApiTypes.OBJECT,
        },
        examples=[    
            OpenApiExample(
                "logoff",
                description="End user session in browser",
                value={
                    'message': 'Sucesso ao finalizar à sessão.',
                    'data': []
                },
                response_only=True,
                status_codes=["200"],
            ),      
        ]
    )
    def post(self, request):
        logout(request)
        return Response({'message': 'Sucesso ao finalizar à sessão.', 'data': []}, status=status.HTTP_200_OK)
