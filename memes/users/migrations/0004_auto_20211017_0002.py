# Generated by Django 3.2.8 on 2021-10-17 00:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20211016_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='profile_img',
            field=models.ImageField(blank=True, default=None, max_length=255, upload_to=users.models.upload_avatar),
        ),
        migrations.CreateModel(
            name='Karma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_created=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
