from django.contrib.auth import get_user
from django.core import serializers
from django.db.models import base
from django.http.response import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render


from django.views.generic import View
from comments.models import MemeComment, MemeCommentKarma

from memes_app.forms import MemeForm
from comments.forms import MemeCommentForm
from memes_app.models import Meme
# Create your views here.

import json


#TODO: limit comments adding to avoid spam
class AddMemeComment(View):
    '''Add comment to meme'''
    def post(self, request, pk):
        if request.method == "POST":
            if request.user.is_authenticated:
                meme = get_object_or_404(Meme, pk=pk)

                form = MemeCommentForm(request.POST)
                if form.is_valid():
                    new_comment = form.save(commit=False)
                    new_comment.original_poster = get_user(request)
                    new_comment.comment_object = meme
                    new_comment.save()
                    return JsonResponse({"success": True, "msg": "Succesfully added new comment"})
                else:
                    return JsonResponse({"success": False, "msg": "Failed adding comment"})
            else:
                return JsonResponse({"success": False, "msg": "No permission"})
        else:
            raise Http404()



class AddReplyComment(View):
    '''Add comment replying to another comment'''
    def post(self, request, pk):
        if request.method == "POST":
            if request.user.is_authenticated:
                parent_comment = get_object_or_404(MemeComment, pk=pk)

                form = MemeCommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.original_poster = get_user(request)
                    comment.comment_object = parent_comment.comment_object
                    '''Comments replies has only 1 level of depth'''
                    if parent_comment.parent_comment != None:
                        comment.parent_comment = parent_comment.parent_comment
                    else:
                        comment.parent_comment = parent_comment
                    comment.save()
                    return JsonResponse({"success": True, "msg": "Succesfully added new comment"})
                else:
                    return JsonResponse({"success": False, "msg": "Failed adding comment"})
            else:
                return JsonResponse({"success": False, "msg": "No permission"})
        else:
            raise Http404()


#TODO: add controls to template
def change_meme_comment_karma(self, request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            comment = get_object_or_404(MemeComment, pk=pk)
            user = get_user(request)

            try:
                given_karma = MemeCommentKarma.objects.get(user=user, comment=comment)
                given_karma.delete()
                comment.karma -= 1   
                comment.save()
                msg =  "Succesfully taken karma away!"
                karma_given = False
            except MemeCommentKarma.DoesNotExist:
                #meme wasnt given karma point by user
                given_karma = MemeCommentKarma(user=user,comment=comment)
                given_karma.save()
                comment.karma += 1
                comment.save()
                msg = "Succesfully fiven karma point"
                karma_given = True

            return JsonResponse({"success": True, "karma_given": karma_given, "karma": comment.karma, "msg": msg})
        else:
            return JsonResponse({"success": False, "msg": "No permission"})

    else:
        raise Http404()



class GetMemeComments(View):
    def post(self, request, pk):
        '''Returns all comments for the meme'''
        meme = get_object_or_404(Meme, pk=pk)
        sort = request.GET.get("sort", default="new")
        
        if sort == "best":
            base_comments = MemeComment.objects.filter(parent_comment=None, comment_object=meme).order_by("-karma", "date_created")
        else:   #if sort == "new"
            base_comments = MemeComment.objects.filter(parent_comment=None, comment_object=meme).order_by("date_created", "-karma")

        comments_data = []
        for base_comm in base_comments:
            comments_data.append(base_comm)
            for reply_comm in base_comm.memecomment_set.all().order_by("date_created", "-karma"):
                comments_data.append(reply_comm)


        serialized_comments = json.loads(serializers.serialize("json", comments_data,  use_natural_foreign_keys=True))
        data = {"success": True, "comments_count": meme.comments_count, "comments": serialized_comments}
        return JsonResponse(data, safe=False)