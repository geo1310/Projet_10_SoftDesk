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
        fields = "__all__"


class IssuePostSerializer(serializers.ModelSerializer):
    """
    Serializer pour les requetes POST de swagger.

    """

    title = serializers.CharField(default="Issue")
    description = serializers.CharField(default="description")
    type = serializers.CharField(default="BUG")
    priority = serializers.CharField(default="LOW")
    progress = serializers.CharField(default="To Do")
    project_assigned = serializers.IntegerField(default=None)
    contributor_assigned = serializers.IntegerField(default=None)

    class Meta:
        """
        Métadonnées du serializer ProjectSerializer.

        Attributes:
            model (class): Classe du modèle à sérialiser (Project).
            fields (tuple): Liste des champs du modèle à inclure dans la sérialisation.
        """

        model = Issue
        exclude = ["author"]
