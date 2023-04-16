from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .serializer import HospitalSerializer
from ..models import Hospital

class HospitalView(generics.GenericAPIView):
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, id=None):
        hospital = Hospital.objects.filter(id=id).first()
        if hospital:
            serializer = self.serializer_class(hospital, data=request.data, context={'user': request.user}, partial=True)
            if not(serializer.is_valid()):
                return Response({'message': 'Falha ao atualizar hospital, verifique os dados inseridos e tente novamente.', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                
            serializer_data = self.serializer_class(serializer.save()).data
            return Response({'message': 'Dados do hospital atualizado.', 'data': serializer_data}, status=status.HTTP_200_OK)
                
        else:
            return Response({'message': 'Hospital não localizado.', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        hospital = Hospital.objects.filter(id=id).first()
        if hospital:
            serializer = self.serializer_class(hospital).data
            hospital.delete()
            return Response({'message': 'Hospital removido.'.format(id), 'data': [serializer]}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Hospital não localizado.'.format(id), 'data': []}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        id = request.query_params.get('id')
        #If the request is not given an ID, data from all hospitals will be retrieved
        #Passing the ID will retrieve the data of the specific ID
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

        serializer_data = self.serializer_class(serializer.save()).data

        return Response({'message': 'Hospital cadastrado.', 'data': [serializer_data]}, status=status.HTTP_201_CREATED)
