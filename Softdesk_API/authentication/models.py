from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date


class CustomUser(AbstractUser):
    """
    Modèle personnalisé d'utilisateur.

    Utilise le modèle d'utilisateur abstrait de Django pour étendre les fonctionnalités de base.

    Attributes:
        username: Nom d'utilisateur unique.
        first_name: Prénom de l'utilisateur.
        last_name: Nom de famille de l'utilisateur.
        email: Adresse e-mail de l'utilisateur.
        password: Mot de passe de l'utilisateur (haché).
        date_joined: Date et heure de création du compte utilisateur.
        is_active: Indique si le compte utilisateur est actif ou non.
        is_staff: Indique si l'utilisateur est membre du personnel ou non.
        is_superuser: Indique si l'utilisateur a tous les droits de l'administrateur ou non.

        date_of_birth: Date de naissance de l'utilisateur.
        can_be_contacted: Booléen indiquant si l'utilisateur peut être contacté ou non.
        can_data_be_shared: Booléen indiquant si les données de l'utilisateur peuvent être partagées ou non.
    """

    date_of_birth = models.DateField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)

    @staticmethod
    def is_over_15(date_of_birth):
        """
        Méthode qui vérifie si l'utilisateur a plus de 15 ans.
        """
        if date_of_birth:
            today = date.today()
            age = (
                today.year
                - date_of_birth.year
                - (
                    (today.month, today.day)
                    < (date_of_birth.month, date_of_birth.day)
                )
            )
            return age > 15
        return False
