# Generated by Django 4.2.5 on 2023-10-09 07:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "supporting_system",
            "0003_characteristics_fit_alter_field_of_study_study_mode_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="characteristics",
            old_name="attribiute",
            new_name="attribute",
        ),
    ]
