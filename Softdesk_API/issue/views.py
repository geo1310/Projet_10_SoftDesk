from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from project.models import Project

from .models import Issue
from .permissions import IsAuthenticatedAndIsAuthor
from .serializers import IssuePostSerializer, IssueSerializer


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Issue.

    """

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticatedAndIsAuthor]

    @swagger_auto_schema(
        request_body=IssuePostSerializer,
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
        serializer.validated_data["author"] = request.user

        # récupère la liste des contributors du projet assigné a l'issue
        project = serializer.validated_data["project_assigned"]
        contributors_project_list = project.contributors.all()

        # Vérifie si le contributeur assigné est dans la liste des contributeurs
        if "contributor_assigned" in serializer.validated_data:
            contributor_assigned = serializer.validated_data["contributor_assigned"]
            if contributor_assigned not in contributors_project_list:
                return Response(
                    {
                        "error": "Le Contributeur assigné doit etre dans les contirbuteurs du projet."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Vérifie si l'auteur est dans la liste des contributeurs
        issue_author = serializer.validated_data["author"]
        if issue_author not in contributors_project_list:
            return Response(
                {
                    "error": "L'auteur de l'issue doit etre dans les contributeurs du projet."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=IssuePostSerializer,
        responses={
            status.HTTP_201_CREATED: IssueSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
            status.HTTP_401_UNAUTHORIZED: "Authentification non trouvée",
            status.HTTP_403_FORBIDDEN: "Vous n'êtes pas autorisé à modifier cette Issue",
            status.HTTP_404_NOT_FOUND: "Issue non trouvée",
        },
    )
    def update(self, request, *args, **kwargs):
        """
        Modification d'une Issue.
        L'utilisateur connecté doit etre l'auteur de l'issue pour pouvoir la modifier.

        Args:
            request (HttpRequest): La requête HTTP contenant les données de mise à jour.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Réponse HTTP indiquant le résultat de la mise à jour.
        """

        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=IssuePostSerializer,
        responses={
            status.HTTP_201_CREATED: IssueSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
            status.HTTP_401_UNAUTHORIZED: "Authentification non trouvée",
            status.HTTP_403_FORBIDDEN: "Vous n'êtes pas autorisé à modifier cette Issue",
            status.HTTP_404_NOT_FOUND: "Issue non trouvée",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Modification partielle d'une Issue.
        L'utilisateur connecté doit etre l'auteur de l'issue pour pouvoir la modifier.

        Args:
            request (HttpRequest): La requête HTTP contenant les données de mise à jour.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Réponse HTTP indiquant le résultat de la mise à jour.
        """

        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "L'issue a été supprimé.",
            status.HTTP_401_UNAUTHORIZED: "Authentification non trouvée",
            status.HTTP_403_FORBIDDEN: "Vous n'êtes pas autorisé à modifier cette issue",
            status.HTTP_404_NOT_FOUND: "Issue non trouvé",
        },
    )
    def destroy(self, request, *args, **kwargs):
        """
        Suppression d'une Issue.
        L'utilisateur connecté doit etre l'auteur de l'Issue pour pouvoir la supprimer

        Args:
            request (HttpRequest): La requête HTTP contenant les données de suppression.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Réponse HTTP indiquant le résultat de la suppression.
        """

        return super().destroy(request, *args, **kwargs)
