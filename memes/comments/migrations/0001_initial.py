# Generated by Django 3.2.8 on 2021-11-23 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memes_app', '0012_alter_meme_original_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemeComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('content', models.CharField(max_length=12000)),
                ('karma', models.IntegerField(blank=True, default=0, verbose_name='Karma points')),
                ('hidden', models.BooleanField(default=False)),
                ('comment_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='memes_app.meme')),
                ('original_poster', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('parent_comment', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='comments.memecomment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MemeCommentKarma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('karma_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.memecomment')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
