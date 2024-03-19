from django.conf import settings
from django.db import models


class Project(models.Model):
    """
    Modèle représentant un projet.

    Attributes:
        title (str): Titre du projet.
        description (str): Description du projet.
        author (ForeignKey): L'auteur du projet.
        contributors (ManyToManyField): Les contributeurs du projet.
        type (str): Type du projet (frontend, backend, ios, android).
        time_created (DateTimeField): Date et heure de création du projet.
    """

    TYPE_CHOICES = [
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("ios", "iOS"),
        ("android", "Android"),
    ]

    title = models.CharField(max_length=128, unique=True)

    description = models.TextField(max_length=2048)

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_project",
        blank=True,
    )

    contributors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, related_name="contributors", blank=True
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")

    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
