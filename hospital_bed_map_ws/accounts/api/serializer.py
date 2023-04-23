from ..models import Users
from rest_framework import serializers

class LoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        validators=[],  # remover validação de unicidade
        max_length=255,
        required=True,
        allow_blank=False
    )

    class Meta:
        model = Users
        fields = ('username', 'password')

    def validate(self, attrs):
        username = attrs.get('username')
        if(not(Users.objects.filter(username=username).exists())):
            raise serializers.ValidationError({'username': 'Usuário não cadastrado.'})
        
        return attrs