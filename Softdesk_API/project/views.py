from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Project.

    Permet d'effectuer des opérations CRUD (Create, Retrieve, Update, Delete)
    sur les instances du modèle Project.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Méthode pour effectuer la création d'une nouvelle instance de projet.

        Cette méthode est appelée lorsqu'une nouvelle instance de projet est sur le point
        d'être créée. Elle permet de personnaliser le processus de création en remplissant
        automatiquement les champs 'author' et 'contributors' avec l'utilisateur connecté
        avant de sauvegarder l'objet dans la base de données.

        Args:
            serializer (ProjectSerializer): Le serializer utilisé pour valider et sauvegarder
                les données de l'instance de projet.

        Returns:
            None
        """

        serializer.save(author=self.request.user)
        serializer.instance.contributors.add(self.request.user)
