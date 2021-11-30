from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

from memes_app.models import Meme


class Comment(models.Model):
    '''Base class for comments. Might be later used to leave comments about e.g. users'''
    date_added      = models.DateTimeField(auto_now_add=True)
    date_edited     = models.DateTimeField(auto_now=True)   #if date_added != date_edited => comment was edited
    original_poster = models.ForeignKey(to=get_user_model(), default=None, null=True, on_delete=models.SET_NULL)
    content         = models.CharField(max_length=12000, null=False, blank=False)
    karma           = models.IntegerField(verbose_name="Karma points", default=0, blank=True, null=False)
    hidden          = models.BooleanField(null=False, default=False)
    parent_comment  = models.ForeignKey(to='self', default=None, null=True, on_delete=models.CASCADE)
    comment_object  = None  #define in child classes! Variable storing reference to commented thing (e.g. meme or user)
    
    class Meta:
        abstract = True

class CommentKarma(models.Model):
    '''Base class for Comments Karma. Might be later used for comments different than users one'''
    date_created    = models.DateTimeField(auto_now_add=True, null=False)
    sender          = models.ForeignKey(to=get_user_model(), null=False, on_delete=models.CASCADE) #TODO: handle karma point change on user account delete
    comment         = None #define in child classes! Variable storing reference to rated comment

    class Meta:
        abstract = True

class MemeComment(Comment):
    comment_object  = models.ForeignKey(to=Meme, null=False, on_delete=models.CASCADE)

class MemeCommentKarma(CommentKarma):
    comment         = models.ForeignKey(to=MemeComment, null=False, on_delete=models.CASCADE)

