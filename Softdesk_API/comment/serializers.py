from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer simplifié pour le modèle Comment.

    """

    class Meta:
        """
        Métadonnées du serializer ProjectSerializer.

        Attributes:
            model (class): Classe du modèle à sérialiser (Project).
            fields (tuple): Liste des champs du modèle à inclure dans la sérialisation.
        """

        model = Comment
        fields = "__all__"


class CommentPostSerializer(serializers.ModelSerializer):
    """
    Serializer pour les requetes POST de swagger.

    """

    title = serializers.CharField(default="Comment")
    description = serializers.CharField(default="description")
    issue_assigned = serializers.IntegerField(default=None)

    class Meta:
        """
        Métadonnées du serializer ProjectSerializer.

        Attributes:
            model (class): Classe du modèle à sérialiser (Project).
            exclude (tuple): Liste des champs du modèle à exclure dans la sérialisation.
        """

        model = Comment
        exclude = ("author",)
