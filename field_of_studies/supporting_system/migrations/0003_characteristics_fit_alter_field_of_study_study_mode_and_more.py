# Generated by Django 4.2.5 on 2023-10-08 12:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supporting_system', '0002_rename_descritpion_field_of_study_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='characteristics',
            name='fit',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='field_of_study',
            name='study_mode',
            field=models.CharField(choices=[('Stacjonarne', 'Stacjonarne'), ('Niestacjonarne', 'Niestacjonarne'), ('Stacjonarne i niestacjonarne', 'Stacjonarne i niestacjonarne')], max_length=30),
        ),
        migrations.AlterField(
            model_name='university',
            name='type',
            field=models.CharField(choices=[('Uniwersytet', 'Uniwersytet'), ('Akademia Wychowania Fizycznego', 'Akademia Wychowania Fizycznego'), ('Uczelnia Ekonomiczna', 'Uczelnia Ekonomiczna'), ('Uczelnia Pedagogiczna', 'Uczelnia Pedagogiczna'), ('Uczelnia Przyrodniczo-Rolnicza', 'Uczelnia Przyrodniczo-Rolnicza'), ('Uczelnia Techniczna', 'Uczelnia Techniczna')], max_length=30),
        ),
    ]
