from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import HospitalSerializer
from ..models import Hospital

class HospitalView(generics.GenericAPIView):
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, id=None):
        hospital = Hospital.objects.filter(id=id).first()
        if hospital:
            serializer = self.serializer_class(hospital, data=request.data, context={'user': request.user}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Hospital atualizado.', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Falha ao atualizar hospital, verifique os dados inseridos e tente novamente.', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Hospital {} não localizado.'.format(id), 'data': []}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        hospital = Hospital.objects.filter(id=id).first()
        if hospital:
            serializer = self.serializer_class(hospital).data
            hospital.delete()
            return Response({'message': 'Hospital {} removido.'.format(id), 'data': [serializer]}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Hospital {} não localizado.'.format(id), 'data': []}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        #Caso a requisição não seja passado um ID, serão recuperados os dados de todos os hospitais
        #Passando o ID será recuperado os dados do ID específico
        if id is None:
            hospitals = Hospital.objects.all()
            serializer = self.serializer_class(hospitals, many=True)
            return Response({'message': 'Lista de hospitais', 'data': serializer.data}, status=status.HTTP_200_OK)
            
        else:
            hospitals = Hospital.objects.filter(id=id).first()
            if hospitals:
                serializer = self.serializer_class(hospitals)
                return Response({'message': 'Hospital {} localizado.'.format(id), 'data': [serializer.data]}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Hospital {} não localizado.'.format(id), 'data':[]}, status=status.HTTP_400_BAD_REQUEST)
            
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})

        if not(serializer.is_valid()):
            return Response({'message': 'Falha ao criar hospital, verifique os dados inseridos e tente novamente.', 'data':[serializer.errors]}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.save()
        serializer_data = self.serializer_class(data).data

        return Response({'message': 'Hospital cadastrado.', 'data': [serializer_data]}, status=status.HTTP_201_CREATED)
