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
        fields = ("title", "description", "type",)

class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Project.

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
