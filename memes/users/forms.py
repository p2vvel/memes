from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm



class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("login", "email")


class MyClearableFileInput(forms.ClearableFileInput):
    '''ClearableFileInput (default widget for ImageFields) with deleted info "Currently: /some/file/path.ext'''
    template_name = "users/forms/MyClearableFileInput.html"

class MyUserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("profile_img", "description")
        widgets = { "profile_img": MyClearableFileInput() }