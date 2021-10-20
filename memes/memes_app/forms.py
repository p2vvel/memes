from django import forms

from memes.images.models import Meme



class ImagesForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ["title", "original_image", "description"]
        