# Generated by Django 3.2.8 on 2021-10-26 17:00

from django.db import migrations, models
import memes_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('memes_app', '0008_memekarma'),
    ]

    operations = [
        migrations.AddField(
            model_name='meme',
            name='normal_image',
            field=models.ImageField(blank=True, max_length=255, upload_to=memes_app.models.upload_meme_normal),
        ),
    ]