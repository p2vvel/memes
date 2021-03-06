# Generated by Django 3.2.8 on 2021-10-16 14:21

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211015_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='description',
            field=models.TextField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='profile_img',
            field=models.ImageField(default=None, upload_to=users.models.upload_avatar),
        ),
    ]
