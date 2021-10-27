from django.contrib.auth import get_user_model
from django.db import models
from django.core.files import File


# Create your models here.

import uuid
import os

from PIL import Image
from io import BytesIO

from .utils import compress_image

def upload_meme_original(instance, filename):
    new_filename = uuid.uuid4()
    ext = os.path.splitext(filename)[1]
    return "memes/original/{filename}{ext}".format(filename=new_filename, ext=ext)

def upload_meme_normal(instance, filename):
    new_filename = uuid.uuid4()
    ext = os.path.splitext(filename)[1]
    return "memes/normal/{filename}{ext}".format(filename=new_filename, ext=ext)


class Meme(models.Model):
    title           = models.CharField(max_length=255, blank=False, null=False)
    description     = models.TextField(max_length=1000, blank=True, null=True, default="")
    date_created    = models.DateTimeField(auto_now_add=True)
    karma           = models.IntegerField(blank=False, null=False, default=0)
    hidden          = models.BooleanField(default=False, blank=True, null=False)
    accepted        = models.BooleanField(default=False, blank=True, null=False)
    data_accepted   = models.DateTimeField(blank=True, null=True)
    original_image  = models.ImageField(max_length=255, blank=False, null=False, upload_to=upload_meme_original)
    normal_image    = models.ImageField(max_length=255, blank=True, null=False, upload_to=upload_meme_normal)

    original_poster = models.ForeignKey(to=get_user_model(), default=None, null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs) -> None:
        '''Have to remember about compressing image while saving it'''
        #compressed image will be saved only on adding
        if self._state.adding:
            #TODO: watermark
            img = Image.open(self.original_image)
            new_image = compress_image(img, 600)
            buffer = BytesIO()
            new_image.save(buffer, format="JPEG", quality=90)
            self.normal_image = File(buffer, name="temp.jpg")



            
        super().save(args, kwargs)

class MemeKarma(models.Model):
    date_created    = models.DateTimeField(auto_now_add=True)
    meme            = models.ForeignKey(to=Meme, on_delete=models.CASCADE, null=False)
    user            = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)