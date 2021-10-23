from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from .forms import MemeForm

from .models import Meme
from django.contrib.auth import get_user, login
from django.contrib.auth.decorators import login_required

from django.views.generic import View

from django.utils.decorators import method_decorator

# Create your views here.


#main site with accepted memes
class MainView(ListView):
    model = Meme
    # paginate_by = 20
    template_name = "memes/main_view.html"
    context_object_name = "memes"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["form"] = MemeForm()
        return context

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
    


