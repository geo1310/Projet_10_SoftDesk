from datetime import date

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
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "can_be_contacted",
            "can_data_be_shared",
        )
        extra_kwargs = {
            "password": {"write_only": True}
        }  # Pour que le mot de passe ne soit pas affiché dans la réponse


class CustomUserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer de détail pour le modèle CustomUser.

    Attributes:
        None
    """

    class Meta:
        """
        Métadonnées du serializer CustomUserSerializer.

        Attributes:
            model (class): Classe du modèle à sérialiser (CustomUser).
            exclude (list): Liste des champs du modèle à exclure dans la sérialisation.
        """

        model = CustomUser
        exclude = [
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
        ]


class CustomUserPostSerializer(serializers.ModelSerializer):
    """
    Serializer pour les requetes POST de swagger.

    """

    username = serializers.CharField(default="")
    password = serializers.CharField(default="")
    date_of_birth = serializers.DateField(default=date.today())
    first_name = serializers.CharField(default="Nom")
    last_name = serializers.CharField(default="Prénom")

    class Meta:
        """
        Métadonnées du serializer ProjectSerializer.

        Attributes:
            model (class): Classe du modèle à sérialiser (Project).
            exclude (tuple): Liste des champs du modèle à exclure
            dans la sérialisation.
        """

        model = CustomUser
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "can_be_contacted",
            "can_data_be_shared",
        )
