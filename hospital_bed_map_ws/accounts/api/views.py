from django.contrib.auth import authenticate, login, logout
from rest_framework import mixins, generics, status, views
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiExample
from .serializer import LoginSerializer
from ..models import Users
from ..utils import get_tokens_for_user
from .examples import LOGIN_RESPONSE_EXAMPLES, LOGIN_REQUESTS

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
            400: OpenApiTypes.OBJECT
        },
        examples=LOGIN_RESPONSE_EXAMPLES,
        request=LOGIN_REQUESTS
    )
    def post(self, request):

        try:
            username = request.data['username']
        except:
            return Response({'message': 'Campo "username" não especificado.', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            password = request.data['password']
        except:
            return Response({'message': 'Campo "password" não especificado.', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        
        '''
        #https://docs.djangoproject.com/en/4.1/topics/auth/default/
        authenticate() method checks if the authentication credentials are valid. returns a User object if
        the credentials are valid for a backend. If credentials are not valid for any backend
        or if a backend throws PermissionDe
        '''        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            '''
            The login() method logs in and saves the user ID to the session, using Django's session framework.
            '''
            login(request, user)
            data = get_tokens_for_user(user)

            return Response({'message': 'Usuário autenticado com sucesso.', 'data': data}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Certifique-se que o usuário ou senha estão corretos.', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

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
