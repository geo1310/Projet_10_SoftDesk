from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Définition de l'objet SchemaView pour swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API SoftDesk Support",
        default_version="v1",
        description="""
        SoftDesk, une société d'édition de logiciels de collaboration, a décidé de publier une application permettant
        de remonter et suivre des problèmes techniques. 
        Cette solution, SoftDesk Support, s’adresse à des entreprises en B2B (Business to Business). 
        """,
        contact=openapi.Contact(email="gbriche59@yahoo.fr"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("authentication.urls")),
    path("", include("project.urls")),
    path("", include("issue.urls")),
    path("", include("comment.urls")),

    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
