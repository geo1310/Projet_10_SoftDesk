from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Issue
from .serializers import IssueSerializer


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Issue.

    """

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: IssueSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Crée un nouveau problème (issue).
        L'auteur du problème est automatiquement défini sur l'utilisateur connecté.

        Args:
            request (HttpRequest): La requête HTTP contenant les données du problème.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Réponse HTTP indiquant le résultat de la création du problème.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "Le problème a été supprimé.",
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        Supprime un problème (issue).
        Seul l'auteur du problème peut le supprimer.

        Args:
            request (HttpRequest): La requête HTTP contenant les données de suppression.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Réponse HTTP indiquant le résultat de la suppression du problème.
        """
        instance = self.get_object()

        if instance.author != self.request.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à supprimer ce problème.")

        return super().destroy(request, *args, **kwargs)
