from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle CustomUser.

    Attributes:
        None
    """

    class Meta:
        """
        Métadonnées du serializer CustomUserSerializer.

        Attributes:
            model (class): Classe du modèle à sérialiser (CustomUser).
            fields (tuple): Liste des champs du modèle à inclure dans la sérialisation.
            extra_kwargs (dict): Options supplémentaires pour les champs spécifiques.
        """

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
