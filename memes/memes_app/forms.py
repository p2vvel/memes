from django import forms

from .models import Meme



class MemeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #simple image format restriction(for normal users at least)
        self.fields['original_image'].widget.attrs.update({'accept': 'image/jpeg, image/png, image/gif'})
    class Meta:
        model = Meme
        fields = ["title", "original_image", "description"]