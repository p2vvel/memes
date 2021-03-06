# Generated by Django 3.2.8 on 2021-10-25 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memes_app', '0007_rename_op_meme_original_poster'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemeKarma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('meme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='memes_app.meme')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
