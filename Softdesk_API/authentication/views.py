from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import CustomUserSerializer
from .models import CustomUser
from .permissions import IsCreationOrIsAuthenticated


class CustomUserViewSet(viewsets.ViewSet):
    """
    Gestion des opérations sur les utilisateurs
    """

    permission_classes = [IsCreationOrIsAuthenticated]

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

        Rélève aussi les erreurs d'intégrité du modele utilisateur:
            La date de naissance de l'utilisateur ne doit pas etre dans le futur.
            L'age de l'utilisateur doit etre supérieur à 15 ans.

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

    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        responses={
            status.HTTP_200_OK: CustomUserSerializer(),
            status.HTTP_400_BAD_REQUEST: "Erreur de validation",
            status.HTTP_403_FORBIDDEN: "Vous n'êtes pas autorisé à mettre à jour cet utilisateur",
            status.HTTP_404_NOT_FOUND: "Utilisateur non trouvé",
        },
    )
    def update(self, request, pk=None):
        """
        Méthode pour modifier un utilisateur existant.
        L'utilisateur peut modifier que ses propres données.

        Args:
            request (HttpRequest): Requête HTTP PATCH ou PUT contenant les données à mettre à jour.
            pk (int): Clé primaire de l'utilisateur à mettre à jour.

        Returns:
            Response: Réponse HTTP contenant les données mises à jour de l'utilisateur ou les erreurs de validation.
        """
        try:
            user = CustomUser.objects.get(pk=pk)
            if (request.user == user):
                serializer = CustomUserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {
                        "error": "Vous n'êtes pas autorisé à mettre à jour cet utilisateur."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        except ObjectDoesNotExist:
            return Response(
                {"error": "L'utilisateur n'existe pas"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "Utilisateur supprimé avec succès",
            status.HTTP_403_FORBIDDEN: "Vous n'êtes pas autorisé à supprimer cet utilisateur",
            status.HTTP_404_NOT_FOUND: "Utilisateur non trouvé",
        },
    )
    def destroy(self, request, pk=None):
        """
        Méthode pour supprimer un utilisateur existant.
        L'utilisateur peut supprimer que ses propres données.

        Args:
            request (HttpRequest): Requête HTTP DELETE.
            pk (int): Clé primaire de l'utilisateur à supprimer.

        Returns:
            Response: Réponse HTTP indiquant si l'utilisateur a été supprimé avec succès ou non.
        """
        try:
            user = CustomUser.objects.get(pk=pk)
            if request.user == user:
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"error": "Vous n'êtes pas autorisé à supprimer cet utilisateur."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
