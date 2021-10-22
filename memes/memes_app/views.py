from django.shortcuts import redirect, render
from django.views.generic import ListView

from .forms import MemeForm

from .models import Meme
# Create your views here.


#main site with accepted memes
class main_view(ListView):
    model = Meme
    # paginate_by = 20
    template_name = "images/main_site.html"
    context_object_name = "memes"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["form"] = MemeForm()
        return context





def meme_add(request):
    # if request.user.is_authenticated() and request.method == "POST":
        # pass
    if request.method == "POST":
        if not request.user.is_authenticated():
            return redirect("index")
        form = MemeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            added_meme = Meme.objects.get()
            return redirect()
    else:
        pass