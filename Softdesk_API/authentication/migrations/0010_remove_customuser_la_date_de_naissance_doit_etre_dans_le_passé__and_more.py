# Generated by Django 5.0.3 on 2024-03-21 12:48

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        (
            "authentication",
            "0009_remove_customuser_la_date_de_naissance_doit_etre_dans_le_passé__and_more",
        ),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="customuser",
            name="La date de naissance doit etre dans le passé !!!",
        ),
        migrations.RemoveConstraint(
            model_name="customuser",
            name="Vous devez avoir plus de 15 ans !!!",
        ),
        migrations.AddConstraint(
            model_name="customuser",
            constraint=models.CheckConstraint(
                check=models.Q(("date_of_birth__lt", datetime.date(2024, 3, 21))),
                name="La date de naissance doit etre dans le passé !!!",
            ),
        ),
        migrations.AddConstraint(
            model_name="customuser",
            constraint=models.CheckConstraint(
                check=models.Q(("date_of_birth__lt", datetime.date(2009, 3, 25))),
                name="Vous devez avoir plus de 15 ans !!!",
            ),
        ),
    ]
