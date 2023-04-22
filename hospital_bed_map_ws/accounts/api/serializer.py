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