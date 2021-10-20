from django.shortcuts import render
from django.views.generic import ListView

from .models import Meme
# Create your views here.


#main site with accepted memes
class main_view(ListView):
    model = Meme
    # paginate_by = 20
    template_name = "images/main_site.html"
    context_object_name = "memes"