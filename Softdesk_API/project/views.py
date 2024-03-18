from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project
from .serializers import (
    ContributorSerializer,
    ProjectDetailSerializer,
    ProjectSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le Modèle Project.
    """

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ProjectSerializer,
        responses={
            status.HTTP_201_CREATED: ProjectSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
        },
        examples={
            "application/json": {
                "title": "string",
                "description": "string",
                "type": "frontend",
                "contributors": [1, 2, 3],
            }
        },
    )
    def create(self, request):
        """
        Création d'un nouveau Projet.
        Author et contributor sont remplis automatiquement avec l'utilisateur connecté.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(author=request.user)
        serializer.instance.contributors.add(request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=ProjectDetailSerializer,
        responses={
            status.HTTP_201_CREATED: ProjectDetailSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
        },
    )
    def update(self, request, *args, **kwargs):
        """
        Modification d'un projet.
        L'utilisateur connecté doit etre l'auteur du projet.

        Args:
            request (HttpRequest): La requête HTTP contenant les données de mise à jour.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Réponse HTTP indiquant le résultat de la mise à jour.
        """
        instance = self.get_object()

        if instance.author != self.request.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à modifier ce projet.")

        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "Le projet a été supprimé.",
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        Suppression d'un projet.
        L'utilisateur connecté doit etre l'auteur du projet.

        Args:
            request (HttpRequest): La requête HTTP contenant les données de suppression.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Réponse HTTP indiquant le résultat de la suppression.
        """
        instance = self.get_object()

        if instance.author != self.request.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à supprimer ce projet.")

        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ContributorSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Le projet avec les contributeurs ajoutés avec succès.",
                schema=ProjectSerializer(),
                examples={
                    "application/json": {
                        "id": 1,
                        "title": "Nom du projet",
                        # Autres champs du projet
                        "contributors": [
                            1,
                            2,
                            3,
                        ],  # Liste des IDs des contributeurs ajoutés
                    }
                },
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Erreur de validation. Le corps de la requête est invalide."
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="Vous n'êtes pas autorisé à ajouter des contributeurs à ce projet."
            ),
        },
    )
    def add_contributors(self, request, pk=None):
        """
        Ajoute des contributeurs à un projet.

        Args:
            request (HttpRequest): La requête HTTP contenant les données de mise à jour.
            pk (int): Clé primaire du projet auquel ajouter les contributeurs.

        Returns:
            Response: Réponse HTTP indiquant le résultat de l'ajout de contributeurs.
        """

        # TODO: Ajouter la logique pour ajouter des contributeurs à un projet.

        pass
