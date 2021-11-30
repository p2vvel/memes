from django import forms
from .models import MemeComment

class MemeCommentForm(forms.ModelForm):
    class Meta:
        model = MemeComment
        fields = ["content"]