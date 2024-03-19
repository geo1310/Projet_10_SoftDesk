from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer simplifié pour le modèle Project.

    """

    class Meta:
        """
        Métadonnées du serializer ProjectSerializer.

        Attributes:
            model (class): Classe du modèle à sérialiser (Project).
            fields (tuple): Liste des champs du modèle à inclure dans la sérialisation.
        """

        model = Project
        fields = "__all__"


class ProjectPostSerializer(serializers.ModelSerializer):
    """
    Serializer pour les requetes POST de swagger.

    """
    title = serializers.CharField(default="")
    description = serializers.CharField(default="")
    type = serializers.CharField(default="frontend")
    contributors = serializers.ListField(default=[])

    class Meta:
        """
        Métadonnées du serializer ProjectSerializer.

        Attributes:
            model (class): Classe du modèle à sérialiser (Project).
            fields (tuple): Liste des champs du modèle à inclure dans la sérialisation.
        """

        model = Project
        exclude = ["author"]

