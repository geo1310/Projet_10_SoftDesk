from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from project.models import Project

from .models import Issue
from .permissions import IsAuthenticatedAndIsAuthor
from .serializers import IssuePostSerializer, IssueSerializer


class IssueViewSet(viewsets.ModelViewSet):
    """
    Gestion des Objets Issue

    Un utilisateur doit etre connecté et authentifié
    Seuls les Issue dont l'utilisateur connecté est contributeur du projet, sont accessibles.
    """

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticatedAndIsAuthor]

    # Liste des Issues dont l'utilisateur est contributeur du projet
    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.filter(contributors=user)
        project_ids = projects.values_list("id", flat=True)

        return Issue.objects.filter(project_assigned__id__in=project_ids)

    @swagger_auto_schema(
        request_body=IssuePostSerializer,
        responses={
            status.HTTP_201_CREATED: IssueSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Création d'une nouvelle Issue

        Un utilisateur doit etre connecté et authentifié
        L'auteur de l'issue doit faire parti des contributeurs du projet concerné.
        L'auteur de l'issue est automatiquement défini sur l'utilisateur connecté.

        Le contributor_assigned est optionnel et doit faire parti des contributeurs du projet concerné.

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

        serializer.save()

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

        Un utilisateur doit etre connecté et authentifié
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

        Un utilisateur doit etre connecté et authentifié
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

        Un utilisateur doit etre connecté et authentifié
        L'utilisateur connecté doit etre l'auteur de l'Issue pour pouvoir la supprimer

        Args:
            request (HttpRequest): La requête HTTP contenant les données de suppression.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Réponse HTTP indiquant le résultat de la suppression.
        """

        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "project_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            status.HTTP_200_OK: IssueSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: "Authentification non trouvée",
            status.HTTP_403_FORBIDDEN: "Vous n'êtes pas autorisé à accéder aux issues de ce projet.",
            status.HTTP_404_NOT_FOUND: "Projet non trouvé.",
        },
    )
    @action(detail=False, methods=["get"], url_path="project-issues")
    def project_issues(self, request):
        """
        Récupère la liste des issues d'un projet spécifique.

        Un utilisateur doit etre connecté et authentifié
        Seuls les projets dont l'utilisateur connecté est contributeur sont accessibles.

        Args:
            project_id (int): L'identifiant du projet.

        Returns:
            QuerySet: Le queryset des issues du projet spécifié.
        """
        project_id = request.query_params.get("project_id")

        # Vérifie si le projet existe
        try:
            project_id = int(project_id)
        except (TypeError, ValueError):
            return Response(
                {"error": "L'identifiant du projet doit être un entier."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not Project.objects.filter(id=project_id).exists():
            return Response(
                {"error": "Projet non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )

        # Vérifie si l'utilisateur est contributeur du projet
        if not Project.objects.filter(
            id=project_id, contributors=self.request.user
        ).exists():
            return Response(
                {
                    "error": "Vous n'êtes pas autorisé à accéder aux issues de ce projet."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Récupère les issues du projet spécifié
        project_issues = Issue.objects.filter(project_assigned_id=project_id)
        serializer = self.get_serializer(project_issues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
