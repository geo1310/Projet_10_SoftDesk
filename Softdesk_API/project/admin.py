from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Administration personnalisée pour le modèle Project.

    Attributes:
        list_display (tuple): Liste des champs à afficher dans la liste des utilisateurs de l'interface admin.
    """

    list_display = (
        "author",
        "title",
        "type",
        "time_created",
        "id",
    )
