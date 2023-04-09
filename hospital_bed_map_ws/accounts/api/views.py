from django.contrib.auth import authenticate, login, logout
from rest_framework import mixins, generics
from rest_framework.response import Response
from rest_framework import status
from .serializer import LoginSerializer
from ..models import Users
from ..utils import get_tokens_for_user

#Classe responsável por realizar autenticação do usuário via api REST
class LoginView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    serializer_class = LoginSerializer

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
        Método authenticate() verifica se as credenciais de autenticação são válidas.retorna um User objeto se 
        as credenciais forem válidas para um back-end. Se as credenciais não forem válidas para nenhum back-end 
        ou se um back-end gerar PermissionDenied, ele retornará None.
        '''        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            '''
            Método login() realiza o login salva o ID do usuário na sessão, usando o framework de sessão do Django.
            '''
            login(request, user)
            data = get_tokens_for_user(user)

            return Response({'message': 'Usuário autenticado com sucesso.', 'data': [data]}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Credencias inválidas', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

#Classe responsável por encerrar a sessão
class LogoutView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    def post(self, request):
        logout(request)
        return Response({'message': 'Sucesso ao finalizar a sessão.', 'data': []}, status=status.HTTP_200_OK)
