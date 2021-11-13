from typing import List
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView

from .forms import MemeForm

from .models import Meme, MemeKarma
from django.contrib.auth import get_user, login
from django.contrib.auth.decorators import login_required

from django.views.generic import View

from django.utils.decorators import method_decorator

from django.urls.base import reverse

from django.utils import timezone

# Create your views here.


#main site with accepted memes
class MainMemeView(ListView):
    model = Meme
    paginate_by = 8
    template_name = "memes/main_view.html"
    context_object_name = "memes"
    ordering = ["-date_accepted"]

    def get_queryset(self):
        data = super().get_queryset()
        return data.filter(accepted=True, hidden=False)
        # data = (self.model.objects.all()
        #     .order_by(*self.ordering)
        #     .filter(accepted=False))
        # return data
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MemeForm()
        return context


class FreshMemeView(MainMemeView):
    template_name = "memes/fresh_view.html"
    ordering = ["-date_created"]
    def get_queryset(self):
        data = super(ListView, self).get_queryset()
        return data.filter(accepted=False, hidden=False)
        # data = (self.model.objects.all()
        #     .order_by(*self.ordering)
        #     .filter(accepted=False, hidden=False))
        # return data


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


class MemeView(DetailView):
    model = Meme
    context_object_name = "meme"
    template_name = "memes/meme_view.html"



def karma_change(request, pk):
    if request.user.is_authenticated:
        user = get_user(request)
        meme = get_object_or_404(Meme, pk=pk)

        try:
            given_karma = MemeKarma.objects.get(user=user, meme=meme)
            given_karma.delete()
            meme.karma -= 1   
            meme.save()
        except MemeKarma.DoesNotExist:
            #meme wasnt given karma point by user
            given_karma = MemeKarma(user=user, meme=meme)
            given_karma.save()
            meme.karma += 1
            meme.save()
        return redirect(reverse("meme_view", args=(meme.pk,)))
    else:
        return redirect(reverse("index"))


#TODO: test this functionality
def visibility_change(request, pk):
    '''Change meme visibility (only available for admin)'''
    if request.user.is_authenticated and request.user.is_superuser:
        meme = get_object_or_404(Meme, pk=pk)

        meme.hidden = not meme.hidden
        meme.save()

        return redirect(reverse("meme_view", args=(meme.pk,)))
    else:
        return redirect("index")


#TODO: test this functionality
def acceptance_change(request, pk):
    '''Change if meme is accepted(visible on main meme listview), available only for admin'''
    if request.user.is_authenticated and request.user.is_superuser:
        meme = get_object_or_404(Meme, pk=pk)

        if not meme.accepted:
            meme.accepted = True
            meme.date_accepted = timezone.now()
            meme.save()
        else:
            meme.accepted = False
            meme.date_accepted = None
            meme.save()
        
        return redirect(reverse("meme_view", args=(meme.pk,)))
    else:
        return redirect("index")