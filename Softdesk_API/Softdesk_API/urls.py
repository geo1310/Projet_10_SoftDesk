from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Définition de l'objet SchemaView
schema_view = get_schema_view(
    openapi.Info(
        title="API SoftDesk Support",
        default_version="v1",
        description="API Description",
        contact=openapi.Contact(email="gbriche59@yahoo.fr"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("authentication.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
