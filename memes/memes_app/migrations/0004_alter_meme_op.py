# Generated by Django 3.2.8 on 2021-10-22 22:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memes_app', '0003_alter_meme_op'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meme',
            name='OP',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
