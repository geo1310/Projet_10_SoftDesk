from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet

router = DefaultRouter()
router.register("project", ProjectViewSet, basename="project")

urlpatterns = [
    path("api/", include(router.urls)),
]
