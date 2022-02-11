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
                    return JsonResponse({"success": True, "msg": "Successfully added new comment"})
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
                    return JsonResponse({"success": True, "msg": "Successfully added new comment"})
                else:
                    return JsonResponse({"success": False, "msg": "Failed adding comment"})
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
        
        if request.user.is_authenticated:
            user = get_user(request)
            for k, c in zip(serialized_comments, comments_data):
                k["fields"]["karma_given"] = str(c.is_karma_given(user))
        else:
            for k in serialized_comments:
                k["fields"]["karma_given"] = "0"
                # comments_data[i].karma_given = 0
        
        data = {"success": True, "comments_count": meme.comments_count, "comments": serialized_comments}
        return JsonResponse(data, safe=False)


def change_meme_comment_karma(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            comment = get_object_or_404(MemeComment, pk=pk)
            user = get_user(request)

            positive = False if request.GET.get("positive") == "False" else True

            try:
                #comment karma already exist
                given_karma = MemeCommentKarma.objects.get(user=user, comment=comment)
                if positive == given_karma.positive:
                    comment.karma += -1 if positive else 1  #if deleting positive comment, have to substract one karma point
                    given_karma.delete()
                    karma_given = 0
                else:
                    comment.karma += 2 if positive else -2   #adding karma with different sign means that you have to add or substract 2 (delete old karma and add news)
                    given_karma.positive = not given_karma.positive
                    given_karma.save()
                    karma_given = 1 if positive else -1
                comment.save()
                msg =  "Successfully changed karma!"
            except MemeCommentKarma.DoesNotExist:
                #meme wasnt given karma point by user
                given_karma = MemeCommentKarma(user=user, comment=comment, positive=positive)
                given_karma.save()
                comment.karma += 1 if positive else -1
                comment.save()
                msg = "Successfully changed karma!"
                karma_given = 1 if positive else -1

            return JsonResponse({"success": True, "karma_given": karma_given, "karma": comment.karma, "msg": msg})
        else:
            return JsonResponse({"success": False, "msg": "No permission"})
    else:
        raise Http404()