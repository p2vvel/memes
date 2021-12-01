from django.contrib.auth import get_user_model
from django.db import models
from django.core.files import File


# Create your models here.

import uuid
import os
from django.conf import settings

from PIL import Image, UnidentifiedImageError
from io import BytesIO


from .utils import add_watermark, get_normal_image, resize_image
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


from django.apps import apps

def upload_meme_original(instance, filename):
    new_filename = uuid.uuid4()
    ext = os.path.splitext(filename)[1]
    return "memes/original/{filename}{ext}".format(filename=new_filename, ext=instance.image_extension)

def upload_meme_normal(instance, filename):
    new_filename = uuid.uuid4()
    new_filename = Path(instance.original_image.file.name).name  #original_image is already saved
    return "memes/normal/{filename}".format(filename=new_filename)


class Meme(models.Model):
    title           = models.CharField(max_length=255, blank=False, null=False)
    description     = models.TextField(max_length=1000, blank=True, null=True, default="")
    date_created    = models.DateTimeField(auto_now_add=True)
    karma           = models.IntegerField(blank=False, null=False, default=0)
    hidden          = models.BooleanField(default=False, blank=True, null=False)
    accepted        = models.BooleanField(default=False, blank=True, null=False)
    date_accepted   = models.DateTimeField(blank=True, null=True)
    original_image  = models.ImageField(max_length=255, blank=False, null=False, upload_to=upload_meme_original)
    normal_image    = models.ImageField(max_length=255, blank=True, null=False, upload_to=upload_meme_normal)

    original_poster = models.ForeignKey(to=get_user_model(), default=None, null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs) -> None:
        '''Have to remember about compressing image while saving it'''
        self.clean()    #clean isn't automatically invoked when calling save on model instance!!!!

        #compressed image will be saved only on adding
        if self._state.adding:
            self.normal_image = get_normal_image(self.original_image)

        super().save(args, kwargs)

    def delete(self, *args, **kwargs):
        '''Added image delete function'''
        for p in [self.original_image.path, self.normal_image.path]:
            path = Path(p)
            path.unlink(missing_ok=True)
        super(Meme, self).delete(args, kwargs)

    def clean(self):
        '''Added image format checking. Only PNG, JPEG and GIF formats allowed'''
        super().clean()
        if self.original_image: #image has to be uploaded
            try:
                img = Image.open(self.original_image)
                if img.format not in ["JPEG", "PNG", "GIF"]:
                    raise ValidationError({"original_image": "Wrong image format!"})
                #storing img extension(PIL format might be different from extension!)
                self.image_extension = {"JPEG": ".jpg", "PNG": ".png", "GIF": ".gif"}[img.format]
            except UnidentifiedImageError:
                raise ValidationError("Wrong image file!")  #raised if 'image' appears to be .pdf, .exe or other non-image file 
            except ValidationError:
                raise   #pass exception up
            except Exception as e:
                raise ValidationError("Error while validating!")    #other errors
        else:
            raise ValidationError({"original_image": "No image uploaded!"})

    @property
    def comments_count(self):
        '''Returns amount of comment for a meme'''
        MemeComment = apps.get_model('comments', 'MemeComment')
        return MemeComment.objects.filter(comment_object=self).count()

    def is_karma_given(self, user: get_user_model()):
        '''Returns True if user gave karma else False'''
        try:
            given_karma = MemeKarma.objects.get(user=user, meme=self)
            return True
        except MemeKarma.DoesNotExist:
            #meme wasnt given karma point by user
            given_karma = MemeKarma(user=user, meme=self)
            return False


class MemeKarma(models.Model):
    date_created    = models.DateTimeField(auto_now_add=True)
    meme            = models.ForeignKey(to=Meme, on_delete=models.CASCADE, null=False)
    user            = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)