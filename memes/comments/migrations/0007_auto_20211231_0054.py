# Generated by Django 3.2.10 on 2021-12-30 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_memecommentkarma_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memecomment',
            name='karma',
        ),
        migrations.RemoveField(
            model_name='memecommentkarma',
            name='value',
        ),
        migrations.AddField(
            model_name='memecommentkarma',
            name='positive',
            field=models.BooleanField(default=True, verbose_name='Karma positive'),
        ),
    ]
