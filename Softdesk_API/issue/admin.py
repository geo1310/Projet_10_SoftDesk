from django.contrib import admin

from .models import Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """
    Administration personnalisée pour le modèle Project.

    Attributes:
        list_display (tuple): Liste des champs à afficher dans la liste des utilisateurs de l'interface admin.
    """

    list_display = (
        "author",
        "title",
        "type",
        "project_assigned",
        "priority",
        "progress",
        "id",
    )
