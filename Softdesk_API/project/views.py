from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Project
from .permissions import IsAuthenticatedAndIsAuthor
from .serializers import ProjectPostSerializer, ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Gestion des objets Project.

    Un utilisateur doit etre connecté et authentifié

    Seuls les Projets dont l'utilisateur connecté est contributeur sont
    accessibles.
    """

    serializer_class = ProjectSerializer

    # Liste des projets dont l'utilisateur est contributeur
    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            return Project.objects.filter(contributors=user)
        else:
            return Project.objects.none()

    permission_classes = [IsAuthenticatedAndIsAuthor]

    @swagger_auto_schema(
        request_body=ProjectPostSerializer,
        responses={
            status.HTTP_201_CREATED: ProjectSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
            status.HTTP_401_UNAUTHORIZED: "Authentification non trouvée",
        },
    )
    def create(self, request):
        """
        Création d'un nouveau Projet.

        Un utilisateur doit etre connecté.
        author et contributors sont remplis automatiquement avec l'utilisateur
        connecté.
        Vous pouvez ajouter des contributors.
        """

        # récupération et validation des donnees de la requete
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # on sauvegarde l'utilisateur connecté comme auteur et contributor
        serializer.save(author=request.user)
        serializer.instance.contributors.add(request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=ProjectPostSerializer,
        responses={
            status.HTTP_201_CREATED: ProjectSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
            status.HTTP_401_UNAUTHORIZED: "Authentification non trouvée",
            status.HTTP_403_FORBIDDEN: "Non autorisé à modifier ce projet",
            status.HTTP_404_NOT_FOUND: "Projet non trouvé",
        },
    )
    def update(self, request, *args, **kwargs):
        """
        Modification d'un projet.

        L'utilisateur connecté doit etre l'auteur du projet pour pouvoir
        le modifier.

        Args:
            request (HttpRequest): La requête HTTP contenant les données.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Réponse HTTP indiquant le résultat de la mise à jour.
        """

        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ProjectPostSerializer,
        responses={
            status.HTTP_201_CREATED: ProjectSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
            status.HTTP_401_UNAUTHORIZED: "Authentification non trouvée",
            status.HTTP_403_FORBIDDEN: "Non autorisé à modifier ce projet",
            status.HTTP_404_NOT_FOUND: "Projet non trouvé",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Modification partielle d'un projet.

        L'utilisateur connecté doit etre l'auteur du projet pour pouvoir
        le modifier.

        Args:
            request (HttpRequest): La requête HTTP contenant les données.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Réponse HTTP indiquant le résultat de la mise à jour.
        """

        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "Le projet a été supprimé.",
            status.HTTP_401_UNAUTHORIZED: "Authentification non trouvée",
            status.HTTP_403_FORBIDDEN: "Non autorisé à modifier ce projet",
            status.HTTP_404_NOT_FOUND: "Projet non trouvé",
        },
    )
    def destroy(self, request, *args, **kwargs):
        """
        Suppression d'un projet.

        L'utilisateur connecté doit etre l'auteur du projet pour pouvoir
        le supprimer

        Args:
            request (HttpRequest): La requête HTTP contenant les données.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Réponse HTTP indiquant le résultat de la suppression.
        """

        return super().destroy(request, *args, **kwargs)
