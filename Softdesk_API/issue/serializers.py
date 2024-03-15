from rest_framework import serializers
from .models import Issue

class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer simplifié pour le modèle Issue.

    """

    class Meta:
        """
        Métadonnées du serializer ProjectSerializer.

        Attributes:
            model (class): Classe du modèle à sérialiser (Project).
            fields (tuple): Liste des champs du modèle à inclure dans la sérialisation.
        """
        model = Issue
        fields = '__all__'
