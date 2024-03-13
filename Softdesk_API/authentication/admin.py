from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """docstring"""

    list_display = (
        "username",
        "date_of_birth",
        "can_be_contacted",
        "can_data_be_shared",
        "id",
    )
