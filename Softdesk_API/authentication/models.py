from django.db.models import CheckConstraint, Q

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date, timedelta


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

    date_of_birth = models.DateField(null=False, blank=False)
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)

    class Meta:

        constraints = [
            CheckConstraint(
                # condition dans la requete __lt : less than
                check=Q(date_of_birth__lt=date.today()),
                name="Votre naissance n'a pas encore eu lieu !!!",
            ),
            CheckConstraint(
                check=Q(date_of_birth__lt=date.today() - timedelta(days=15 * 365)),
                name="Vous devez avoir plus de 15 ans !!!",
            ),
        ]
