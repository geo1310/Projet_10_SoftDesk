from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from issue.models import Issue
from project.models import Project

from .models import Comment
from .permissions import IsAuthenticatedAndIsAuthor
from .serializers import CommentPostSerializer, CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Gestion des Objets Comment

    Un utilisateur doit etre connecté et authentifié
    Seuls les Comments dont l'utilisateur connecté est contributeur du projet concerné, sont accessibles.

    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedAndIsAuthor]

    # Liste des Comments dont l'utilisateur est contributeur du projet concerné
    def get_queryset(self):

        if self.request.user.is_authenticated:
            user = self.request.user
            projects = Project.objects.filter(contributors=user)
            project_ids = projects.values_list("id", flat=True)
            issues = Issue.objects.filter(project_assigned__id__in=project_ids)
            issues_ids = issues.values_list("id", flat=True)
            return Comment.objects.filter(issue_assigned__id__in=issues_ids)
        else:
            return Comment.objects.none()

    @swagger_auto_schema(
        request_body=CommentPostSerializer,
        responses={
            status.HTTP_201_CREATED: CommentSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Création d'un nouveau Comment

        Un utilisateur doit etre connecté et authentifié
        L'auteur du comment doit faire parti des contributeurs du projet concerné.
        L'auteur du comment est automatiquement défini sur l'utilisateur connecté.

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

        # Vérifie si l'auteur est dans la liste des contributeurs du projet concerné
        issue = serializer.validated_data["issue_assigned"]
        project = issue.project_assigned
        contributors_project_list = project.contributors.all()

        comment_author = serializer.validated_data["author"]
        if comment_author not in contributors_project_list:
            return Response(
                {
                    "error": "L'auteur du Comment doit etre dans les contributeurs du projet concerné."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=CommentPostSerializer,
        responses={
            status.HTTP_201_CREATED: CommentSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
            status.HTTP_401_UNAUTHORIZED: "Authentification non trouvée",
            status.HTTP_403_FORBIDDEN: "Vous n'êtes pas autorisé à modifier ce Comment",
            status.HTTP_404_NOT_FOUND: "Comment non trouvée",
        },
    )
    def update(self, request, *args, **kwargs):
        """
        Modification d'un Comment.

        Un utilisateur doit etre connecté et authentifié
        L'utilisateur connecté doit etre l'auteur du Comment pour pouvoir le modifier.

        Args:
            request (HttpRequest): La requête HTTP contenant les données de mise à jour.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Réponse HTTP indiquant le résultat de la mise à jour.
        """

        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CommentPostSerializer,
        responses={
            status.HTTP_201_CREATED: CommentSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
            status.HTTP_401_UNAUTHORIZED: "Authentification non trouvée",
            status.HTTP_403_FORBIDDEN: "Vous n'êtes pas autorisé à modifier ce Comment",
            status.HTTP_404_NOT_FOUND: "Comment non trouvée",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Modification partielle d'un Comment.

        Un utilisateur doit etre connecté et authentifié
        L'utilisateur connecté doit etre l'auteur du comment pour pouvoir le modifier.

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
            status.HTTP_204_NO_CONTENT: "Le Comment a été supprimé.",
            status.HTTP_401_UNAUTHORIZED: "Authentification non trouvée",
            status.HTTP_403_FORBIDDEN: "Vous n'êtes pas autorisé à modifier ce Comment",
            status.HTTP_404_NOT_FOUND: "Comment non trouvée",
        },
    )
    def destroy(self, request, *args, **kwargs):
        """
        Supprime un Comment

        Un utilisateur doit etre connecté et authentifié
        Seul l'auteur du Comment peut le supprimer.

        Args:
            request (HttpRequest): La requête HTTP contenant les données de suppression.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments nommés supplémentaires.

        Returns:
            Response: Réponse HTTP indiquant le résultat de la suppression du problème.
        """

        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "issue_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            status.HTTP_200_OK: CommentSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: "Authentification non trouvée",
            status.HTTP_403_FORBIDDEN: "Vous n'êtes pas autorisé à accéder aux comments de ce projet.",
            status.HTTP_404_NOT_FOUND: "Issue non trouvé.",
        },
    )
    @action(detail=False, methods=["get"], url_path="issue-comments")
    def issue_comments(self, request):
        """
        Récupère la liste des Comments d'une issue spécifique.

        Un utilisateur doit etre connecté et authentifié
        Seuls les comments dont l'utilisateur connecté est contributeur du projet concerné, sont accessibles.

        Args:
            issue_id (int): L'identifiant de l' Issue.

        Returns:
            QuerySet: Le queryset des comments de l'issue spécifiée.
        """
        issue_id = request.query_params.get("issue_id")

        # Vérifie si l'Issue existe
        try:
            issue_id = int(issue_id)
        except (TypeError, ValueError):
            return Response(
                {"error": "L'identifiant de l'Issue doit être un entier."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not Issue.objects.filter(id=issue_id).exists():
            return Response(
                {"error": "Issue non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )

        # Vérifie si l'utilisateur est contributeur du projet concerné
        issue_project = Issue.objects.get(id=issue_id).project_assigned
        if not issue_project.contributors.filter(id=request.user.id).exists():
            return Response(
                {
                    "error": "Vous n'êtes pas autorisé à accéder aux Comments de ce projet."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Récupère les Comments de l'Issue spécifié
        issues_comments = Comment.objects.filter(issue_assigned_id=issue_id)
        serializer = self.get_serializer(issues_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
