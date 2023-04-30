from rest_framework import serializers
from ..models import Hospital

class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = ('id', 'name', 'acronym', 'is_active', )

    def validate_name(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('O nome do hospital informado é relativamente curto.')
        return value
    
    def save(self, **kwargs):
        hospital = self.instance

        if(hospital): #if the data is updated 
            hospital.name = self.validated_data.get('name', hospital.name)
            hospital.acronym = self.validated_data.get('acronym', hospital.acronym)
            hospital.is_active = self.validated_data.get('is_active', hospital.is_active)
            hospital.author = self.context['user']
            hospital.save()

        else: #if the data is new
            hospital = Hospital(
                name=self.validated_data['name'],
                acronym=self.validated_data['acronym'],
                is_active=self.validated_data['is_active'],
                author=self.context['user']
            )
            hospital.save()

        return hospital
        