from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsAuthenticatedAndIsAuthor(BasePermission):
    """
    Permission personnalisée :

    1. L'utilisateur doit être authentifié.
    2. Pour les actions de modification et suppression, l'utilisateur doit être l'auteur de la ressource
    concernée.
    """

    def has_permission(self, request, view):
        """
        Méthode pour vérifier si l'utilisateur a la permission d'accéder à la vue.

        Args:
            request (Request): L'objet de requête entrant.
            view (APIView): La vue sur laquelle la permission est vérifiée.

        Returns:
            bool: True si l'utilisateur a la permission.
        """

        if request.user.is_authenticated:
            if view.action in ["list", "create", "retrieve"]:
                return True
            elif view.action in ["update", "partial_update", "destroy"]:
                project = view.get_object()
                if project.author == request.user:
                    return True
                else:
                    raise PermissionDenied(
                        "Vous n'êtes pas autorisé à modifier ou à supprimer ce projet."
                    )

        return False
