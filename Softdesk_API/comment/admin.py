from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Administration personnalisée pour le modèle Comment.

    Attributes:
        list_display (tuple): Liste des champs à afficher dans la liste des utilisateurs de l'interface admin.
    """

    list_display = (
        "author",
        "issue_assigned",
        "time_created",
        "id",
    )

