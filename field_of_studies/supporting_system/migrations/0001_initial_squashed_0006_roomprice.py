# Generated by Django 4.2.5 on 2023-12-03 20:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    replaces = [
        ("supporting_system", "0001_initial"),
        ("supporting_system", "0002_rename_descritpion_field_of_study_description"),
        (
            "supporting_system",
            "0003_characteristics_fit_alter_field_of_study_study_mode_and_more",
        ),
        ("supporting_system", "0004_rename_attribiute_characteristics_attribute"),
        ("supporting_system", "0005_rename_attribiutes_attributes_and_more"),
        ("supporting_system", "0006_roomprice"),
    ]

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Subjects",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subject",
                    models.CharField(default="Nieznany Przedmiot", max_length=80),
                ),
            ],
            options={
                "verbose_name_plural": "Subjects",
            },
        ),
        migrations.CreateModel(
            name="University",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(default="Nieznany Uniwersytet", max_length=200),
                ),
                ("city", models.CharField(default="Nieznane Miasto", max_length=50)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Uniwersytet", "Uniwersytet"),
                            (
                                "Akademia Wychowania Fizycznego",
                                "Akademia Wychowania Fizycznego",
                            ),
                            ("Uczelnia Ekonomiczna", "Uczelnia Ekonomiczna"),
                            ("Uczelnia Pedagogiczna", "Uczelnia Pedagogiczna"),
                            (
                                "Uczelnia Przyrodniczo-Rolnicza",
                                "Uczelnia Przyrodniczo-Rolnicza",
                            ),
                            ("Uczelnia Techniczna", "Uczelnia Techniczna"),
                        ],
                        max_length=30,
                    ),
                ),
                ("rank_overall", models.IntegerField(default=0)),
                ("rank_in_type", models.IntegerField(default=0)),
                (
                    "link_to_site",
                    models.CharField(default="Brak linku do strony", max_length=255),
                ),
            ],
            options={
                "verbose_name_plural": "Universities",
            },
        ),
        migrations.CreateModel(
            name="Field_of_Study",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="Nieznane studia", max_length=100)),
                (
                    "degree",
                    models.CharField(
                        choices=[
                            ("Licencjat", "Licencjat"),
                            ("Inżynier", "Inżynier"),
                            ("Magister", "Magister"),
                            ("Jednolite", "Jednolite"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "study_mode",
                    models.CharField(
                        choices=[
                            ("Stacjonarne", "Stacjonarne"),
                            ("Niestacjonarne", "Niestacjonarne"),
                            (
                                "Stacjonarne i niestacjonarne",
                                "Stacjonarne i niestacjonarne",
                            ),
                        ],
                        max_length=30,
                    ),
                ),
                ("language", models.CharField(default="Polski", max_length=20)),
                ("description", models.TextField(max_length=1000)),
                (
                    "link_to_site",
                    models.CharField(default="Brak linku do strony", max_length=255),
                ),
                (
                    "university",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supporting_system.university",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Field of Studies",
            },
        ),
        migrations.CreateModel(
            name="Exam_Subjects",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "field_of_study",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supporting_system.field_of_study",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supporting_system.subjects",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Exam Subjects",
            },
        ),
        migrations.CreateModel(
            name="Alternative_Exam_Subjects",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "main_subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supporting_system.exam_subjects",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supporting_system.subjects",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Alternative Exam Subjects",
            },
        ),
        migrations.CreateModel(
            name="Characteristics",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supporting_system.attribiutes",
                    ),
                ),
                (
                    "field_of_study",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supporting_system.field_of_study",
                    ),
                ),
                (
                    "fit",
                    models.FloatField(
                        default=0.0,
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ],
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Characteristics",
            },
        ),
        migrations.CreateModel(
            name="Attributes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attribute",
                    models.CharField(default="Nieznana cecha", max_length=120),
                ),
            ],
            options={
                "verbose_name_plural": "Attributes",
            },
        ),
        migrations.CreateModel(
            name="RoomPrice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "avg_room_price",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supporting_system.university",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Room Prices",
            },
        ),
    ]
