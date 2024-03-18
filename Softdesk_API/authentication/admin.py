from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Administration personnalisée pour le modèle CustomUser.

    Cette classe permet de personnaliser l'interface d'administration Django pour le modèle CustomUser.

    Attributes:
        list_display (tuple): Liste des champs à afficher dans la liste des utilisateurs de l'interface admin.
    """

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "date_of_birth",
                    "can_be_contacted",
                    "can_data_be_shared",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "date_of_birth",
                    "password1",
                    "password2",
                    "can_be_contacted",
                    "can_data_be_shared",
                ),
            },
        ),
    )

    list_display = (
        "username",
        "date_of_birth",
        "can_be_contacted",
        "can_data_be_shared",
        "id",
    )
