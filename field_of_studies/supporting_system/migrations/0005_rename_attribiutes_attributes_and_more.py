# Generated by Django 4.2.5 on 2023-10-09 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supporting_system', '0004_rename_attribiute_characteristics_attribute'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Attribiutes',
            new_name='Attributes',
        ),
        migrations.AlterModelOptions(
            name='attributes',
            options={'verbose_name_plural': 'Attributes'},
        ),
        migrations.RenameField(
            model_name='attributes',
            old_name='attribiute',
            new_name='attribute',
        ),
    ]
