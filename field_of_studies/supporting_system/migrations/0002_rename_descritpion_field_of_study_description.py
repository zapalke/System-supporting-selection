# Generated by Django 4.2.5 on 2023-10-06 07:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("supporting_system", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="field_of_study",
            old_name="descritpion",
            new_name="description",
        ),
    ]
