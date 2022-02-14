from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import os
import uuid

from PIL import Image
from io import BytesIO
from django.core.files.base import File

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, login, password=None):
        """Used by python manage.py createuser"""
        if not email:
            raise ValueError('Users must have a login')
        if not login:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), login=login, password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, login, password=None):
        """Used by python manage.py createsuperuser"""
        user = self.create_user(email, login, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


def upload_avatar(instance, filename):
    ext = ".jpg"    # saving all avatars in JPEG format    #ext=os.path.splitext(filename)[1]
    new_filename = uuid.uuid4()
    return "avatars/{filename}{ext}".format(filename=new_filename, ext=ext)


class MyUser(AbstractBaseUser):
    email           = models.CharField(max_length=255, null=False, blank=False, unique=True)
    login           = models.CharField(max_length=60, null=False, blank=False, unique=True)
    karma           = models.IntegerField(verbose_name="Karma points",default=0, null=False)
    date_created    = models.DateTimeField(verbose_name="Registration date", auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)
    # TODO: profile image compression and resizing
    profile_img     = models.ImageField(max_length=255, default=None, upload_to=upload_avatar, blank=True)
    description     = models.TextField(default="", max_length=1000, null=True, blank=True)


    USERNAME_FIELD  = 'email'
    EMAIL_FIELD     = 'email'
    REQUIRED_FIELDS = ['login']                     #USERNAME_FIELD and password are always required!

    is_active       = models.BooleanField(verbose_name="Active", default=True)
    is_superuser    = models.BooleanField(verbose_name="Superuser", default=False)

    objects = MyUserManager()

    def __str__(self):
        return self.login

    # required to make default auth backend to work
    def has_perm(self, perm, obj=None):
        return True

    # required to make default auth backend to work
    def has_module_perms(self, app_label):
        return True

    # required to make default auth backend to work
    @property
    def is_staff(self):
        return self.is_superuser

    def delete(self, *args, **kwargs):
        """Remember about deleting"""
        try:
            os.remove(self.profile_img.path)
        except FileNotFoundError:
            print("User profile already deleted")
        super().delete(args, kwargs)

    def natural_key(self) -> str:
        # used for serialization in comment model
        if self.profile_img:
            key = (self.login, self.profile_img.url)
        else:
            key = (self.login, False)
        return key
        # return (self.login#super().natural_key()

    def __init__(self, *args, **kwargs):
        super(MyUser, self).__init__(*args, **kwargs)
        self.old_profile_img = self.profile_img     # pre_save signal isn't received at creation

    def save(self, *args, **kwargs):
        """Resizing profile picture"""
        # old_profile_img is set in signals.py at pre_save
        if self.profile_img and self.profile_img != self.old_profile_img:
            avatar = Image.open(self.profile_img).convert("RGB")
            avatar.thumbnail((200, 200))
            buffer = BytesIO()
            avatar.save(buffer, name=self.profile_img.name, format="JPEG")
            self.profile_img = File(buffer, name = self.profile_img.name)
        return super().save(*args, **kwargs)


class Karma(models.Model):
    date_created    = models.DateTimeField(auto_now_add=True)
    sender          = models.ForeignKey(to=get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name="sender")
    recipient       = models.ForeignKey(to=get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name="recipient")