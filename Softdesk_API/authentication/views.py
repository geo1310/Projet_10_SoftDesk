from rest_framework import viewsets, status
from rest_framework.response import Response

from django.db import IntegrityError

from drf_yasg.utils import swagger_auto_schema

from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ViewSet):
    """
    Gestion des opérations sur les utilisateurs
    """

    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        responses={
            status.HTTP_201_CREATED: CustomUserSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
        },
    )
    def create(self, request):
        """
        Méthode pour créer un nouvel utilisateur.

        Cette méthode reçoit les données de la requête HTTP POST et valide ces données.
        Rélève aussi les erreurs d'intégrité du modele utilisateur.

        Args:

            request (HttpRequest): Requête HTTP POST contenant les données de l'utilisateur.

        Returns:
            Response: Réponse HTTP contenant les données de l'utilisateur créé ou les erreurs de validation.
        """
        serializer = CustomUserSerializer(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
