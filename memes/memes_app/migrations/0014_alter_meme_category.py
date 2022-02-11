# Generated by Django 3.2.10 on 2022-01-02 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memes_app', '0013_auto_20220102_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meme',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='memes_app.category'),
        ),
    ]
