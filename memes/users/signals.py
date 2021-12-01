from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import MyUser

@receiver(pre_save, sender=MyUser, weak=False)
def on_change(sender, instance: MyUser, **kwargs):
    '''Saves current state of users profile img, so I dont have to change it on every save() call'''
    instance.old_profile_img = instance.profile_img

