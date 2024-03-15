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
        fields = ("title", "description", "type", "contributors")

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


class ContributorSerializer(serializers.Serializer):
    """
    Serializer pour la liste des contributeurs à ajouter à un projet.
    """
    contributors = serializers.ListField(child=serializers.IntegerField())