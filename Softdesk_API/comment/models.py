from django.conf import settings
from django.db import models

from issue.models import Issue


class Comment(models.Model):
    """
    Modèle représentant un commentaire sur un problème (issue).

    Attributes:
        author (ForeignKey): L'utilisateur qui a créé le commentaire.
        description (str): Description détaillée du commentaire.
        issue_assigned (ForeignKey): Problème associé auquel le commentaire est lié.
        time_created (DateTimeField): Date et heure de création du commentaire.
    """

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_comment",
        blank=True,
    )

    title = models.CharField(max_length=128, unique=True)

    description = models.TextField(max_length=2048)

    issue_assigned = models.ForeignKey(
        to=Issue,
        related_name="issue_assigned",
        on_delete=models.CASCADE,
        blank=True,
    )

    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
