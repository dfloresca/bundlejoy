# Generated by Django 5.0.1 on 2024-02-27 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0009_remove_comment_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
