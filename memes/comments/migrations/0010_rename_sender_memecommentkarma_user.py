# Generated by Django 3.2.10 on 2021-12-31 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0009_memecommentkarma_positive'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memecommentkarma',
            old_name='sender',
            new_name='user',
        ),
    ]
