from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import ProjectViewSet

router = DefaultRouter()
router.register("project", ProjectViewSet, basename="project")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "project/<int:pk>/add_contributors/",
        ProjectViewSet.as_view({"post": "add_contributors"}),
        name="add_contributors",
    ),
]
