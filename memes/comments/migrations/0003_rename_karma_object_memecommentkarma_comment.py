# Generated by Django 3.2.8 on 2021-11-24 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_alter_memecomment_parent_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memecommentkarma',
            old_name='karma_object',
            new_name='comment',
        ),
    ]
