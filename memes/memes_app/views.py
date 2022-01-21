from datetime import datetime, timedelta
from typing import List
from django.http.response import Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView

from .forms import MemeForm

from .models import Category, Meme, MemeKarma
from django.contrib.auth import get_user, login
from django.contrib.auth.decorators import login_required

from django.views.generic import View

from django.utils.decorators import method_decorator

from django.urls.base import reverse


from django.http import JsonResponse
from django.utils import timezone


from comments.forms import MemeCommentForm
# Create your views here.

from django.db.models import Q


#main site with accepted memes
class MainMemeView(ListView):
    model = Meme
    paginate_by = 8
    template_name = "memes/main_view.html"
    context_object_name = "memes"
    ordering = ["-date_accepted"]

    def get_queryset(self):
        user = get_user(self.request)
        data = super().get_queryset()
        data =  data.filter(accepted=True, hidden=False)
        if self.request.user.is_authenticated:
            for k in data:
                k.karma_given = k.is_karma_given(user)
        else:
            for k in data:
                k.karma_given = False

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MemeForm()
        return context


class FreshMemeView(MainMemeView):
    template_name = "memes/fresh_view.html"
    ordering = ["-date_created"]
    def get_queryset(self):
        user = get_user(self.request)
        data = super(ListView, self).get_queryset()
        data = data.filter(accepted=False, hidden=False)
        if self.request.user.is_authenticated:
            for k in data:
                k.karma_given = k.is_karma_given(user)
        else:
            for k in data:
                k.karma_given = False
        return data

class MemeView(DetailView):
    model = Meme
    context_object_name = "meme"
    template_name = "memes/meme_view.html"


    def get_context_data(self, **kwargs):
        user = get_user(self.request)
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["meme"].karma_given = context["meme"].is_karma_given(user)
        else:
            context["meme"].karma_given = False
        context["form"] = MemeCommentForm()
        return context
    

class NewFreshView(ListView):
    model = Meme
    
    def get_queryset(self):
        if self.request.is_authenticated:
            data = self.model.objects.filter(accepted=False)    #for logged users everything is visible
        else:
            data = self.model.objects.filter(accepted=False, category__public=True)    #first filtering


        chosen_categories = self.request.GET.getlist("category") #getting categories
        try:
            chosen_categories[chosen_categories.index("none")] = None   #replace "none" string with real none value
        except ValueError:
            pass    #nothing to do if user doesnt want to see main memes (those without assigned category), error raised if "none" not in chosen categoriess
        
        if chosen_categories != []:
            categories_filter = Q()
            for k in chosen_categories:
                categories_filter |= Q(category__slug_iexact=k)
            data = data.filter(accepted=False).filter(categories_filter)
        
        
        sort_method = self.request.GET.get("sort", "new")
        if sort_method == "best":
            data = data.order_by("-karma")
        elif sort_method == "best12":
            time_delta = datetime.now() - timedelta(hours=12)
            data = data.order_by("-karma").filter(date_added__gte=time_delta)
        elif sort_method == "best72":
            time_delta = datetime.now() - timedelta(days=3)
            data = data.order_by("-karma").filter(date_added__gte=time_delta)
        else:# sort_method == "new":
            data = data.order_by("-date_created")

        return data


            



class MemeAdd(View):
    @method_decorator(login_required)
    def get(self, request):
        context = {"form": MemeForm()}
        return render(request, "memes/meme_add_view.html", context)   

    def post(self, request):
        if request.user.is_authenticated:
            form = MemeForm(request.POST, request.FILES)
            #TODO: message about failing meme add
            if form.is_valid():
                new_meme = form.save(commit=False)
                new_meme.original_poster = get_user(request)
                new_meme.save()
                return redirect("meme_view", pk=new_meme.pk)
        return redirect("index")





def karma_change(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = get_user(request)
            meme = get_object_or_404(Meme, pk=pk)

            try:
                given_karma = MemeKarma.objects.get(user=user, meme=meme)
                given_karma.delete()
                meme.karma -= 1   
                meme.save()
                msg =  "Succesfully taken karma away!"
                karma_given = False
            except MemeKarma.DoesNotExist:
                #meme wasnt given karma point by user
                given_karma = MemeKarma(user=user, meme=meme)
                given_karma.save()
                meme.karma += 1
                meme.save()
                msg = "Succesfully fiven karma point"
                karma_given = True

            return JsonResponse({"success": True, "karma_given": karma_given, "karma": meme.karma, "msg": msg})
        else:
            return JsonResponse({"success": False, "msg": "Log in to vote!"})
    else:
        raise Http404()


def visibility_change(request, pk) -> JsonResponse:
    '''Change meme visibility (only available for admin)'''
    if request.method == "POST":
        if request.user.is_authenticated and request.user.is_superuser:
            meme = get_object_or_404(Meme, pk=pk)

            meme.hidden = not meme.hidden
            meme.save()

            # return redirect(reverse("meme_view", args=(meme.pk,)))
            msg = "Succesfully set meme visible" if meme.hidden else "Succesfully hidden meme"
            return JsonResponse({"success": True, "hidden": meme.hidden, "msg": msg})
        else:
            # return redirect("index")
            return JsonResponse({"success": False, "msg": "No permission!"})
    else:
        raise Http404()


def acceptance_change(request, pk) -> JsonResponse:
    '''Change if meme is accepted(visible on main meme listview), available only for admin'''
    if request.method == "POST":
        if request.user.is_authenticated and request.user.is_superuser:
            meme = get_object_or_404(Meme, pk=pk)

            if not meme.accepted:
                meme.accepted = True
                meme.date_accepted = timezone.now()
                meme.save()
                msg = "Succesfully accepted meme"
            else:
                meme.accepted = False
                meme.date_accepted = None
                meme.save()
                msg = "Succesfully reversed meme acceptance"
            
            return JsonResponse({"success": True, "accepted": meme.accepted, "msg": msg})
            # return redirect(reverse("meme_view", args=(meme.pk,)))
        else:
            # return JsonResponse({"success": False, "msg": "Failed to change acceptance"})
            return JsonResponse({"success": False, "msg": "No permission!"})
            # return redirect("index")
    else:
        raise Http404()