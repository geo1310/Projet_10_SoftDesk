from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ViewSet):
    """
    ViewSet personnalisé pour gérer les opérations sur les utilisateurs.

    Cette classe gère la création de nouveaux utilisateurs en vérifiant
    si l'utilisateur a plus de 15 ans avant de l'enregistrer dans la base de données.
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

        Cette méthode reçoit les données de la requête HTTP POST, valide ces données,
        vérifie si l'utilisateur a plus de 15 ans, puis enregistre l'utilisateur
        dans la base de données si les données sont valides.

        Args:

            request (HttpRequest): Requête HTTP POST contenant les données de l'utilisateur.

        Returns:
            Response: Réponse HTTP contenant les données de l'utilisateur créé ou les erreurs de validation.
        """
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():

            # Vérifie l'âge de l'utilisateur
            date_of_birth = serializer.validated_data.get("date_of_birth")

            if date_of_birth and not CustomUser.is_over_15(date_of_birth):

                return Response(
                    {"error": "L'utilisateur doit avoir plus de 15 ans."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
