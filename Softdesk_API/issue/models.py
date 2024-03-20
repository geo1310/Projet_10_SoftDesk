from django.conf import settings
from django.db import models

from project.models import Project


class Issue(models.Model):
    """
    Modèle représentant un problème (issue) dans un projet.
    Attributes:
        TYPE_CHOICES (list): Choix disponibles pour le type de problème.
        TYPE_PRIORITY (list): Choix disponibles pour la priorité du problème.
        TYPE_PROGRESS (list): Choix disponibles pour l'état d'avancement du problème.
        title (str): Titre du problème.
        description (str): Description détaillée du problème.
        author (ForeignKey): L'auteur du problème.
        project_assigned (ForeignKey): Le projet auquel le problème est assigné.
        contributor_assigned (ForeignKey): L'utilisateur attribué au problème.
        type (str): Type du problème (BUG, FEATURE, TASK).
        priority (str): Priorité du problème (LOW, MEDIUM, HIGH).
        progress (str): État d'avancement du problème (To Do, In Progress, Finished).
        time_created (DateTimeField): Date et heure de création du problème.
    """

    TYPE_CHOICES = [
        ("BUG", "BUG"),
        ("FEATURE", "FEATURE"),
        ("TASK", "TASK"),
    ]
    TYPE_PRIORITY = [
        ("LOW", "LOW"),
        ("MEDIUM", "MEDIUM"),
        ("HIGH", "HIGH"),
    ]
    TYPE_PROGRESS = [
        ("To Do", "To Do"),
        ("In Progress", "In Progress"),
        ("Finished", "Finished"),
    ]
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=2048, blank=True)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_issue",
        blank=True,
    )
    project_assigned = models.ForeignKey(
        to=Project,
        related_name="project_assigned",
        on_delete=models.CASCADE,
        blank=True,
    )
    contributor_assigned = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="contributor_assigned",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    priority = models.CharField(
        max_length=20, choices=TYPE_PRIORITY, verbose_name="Priority"
    )
    progress = models.CharField(
        max_length=20, choices=TYPE_PROGRESS, verbose_name="Progress"
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
