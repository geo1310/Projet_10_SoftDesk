from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ViewSet):

    def create(self, request):

        serializer = CustomUserSerializer(data=request.data)
        
        if serializer.is_valid():

            # Vérifie l'âge de l'utilisateur
            date_of_birth = serializer.validated_data.get("date_of_birth")

            if date_of_birth and not CustomUser.is_over_15(date_of_birth):

                return Response(
                    {"error": "L'utilisateur doit avoir au moins 15 ans."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
