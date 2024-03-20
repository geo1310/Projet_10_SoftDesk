from rest_framework.permissions import BasePermission


class IsCreationOrIsAuthenticated(BasePermission):
    """
    Permission personnalisée
    
    1. L'utilisateur doit être authentifié pour toute action, sauf la création.
    2. Pour l'action de création, l'accès est autorisé sans authentification.
    """

    def has_permission(self, request, view):
        return view.action == "create" or request.user.is_authenticated
