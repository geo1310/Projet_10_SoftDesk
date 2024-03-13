from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password",
            "date_of_birth",
            "can_be_contacted",
            "can_data_be_shared",
        )
        extra_kwargs = {
            "password": {"write_only": True}
        }  # Pour que le mot de passe ne soit pas affiché dans la réponse
