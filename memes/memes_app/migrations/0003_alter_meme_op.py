# Generated by Django 3.2.8 on 2021-10-22 22:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memes_app', '0002_meme_op'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meme',
            name='OP',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
