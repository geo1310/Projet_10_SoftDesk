from django.contrib import admin

from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Administration personnalisée pour le modèle CustomUser.

    Cette classe permet de personnaliser l'interface d'administration Django pour le modèle CustomUser.

    Attributes:
        list_display (tuple): Liste des champs à afficher dans la liste des utilisateurs de l'interface admin.
    """

    list_display = (
        "username",
        "date_of_birth",
        "can_be_contacted",
        "can_data_be_shared",
        "id",
    )
