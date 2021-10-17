from logging import log
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, get_user, get_user_model, login
from django.contrib.auth.decorators import login_required

from users.forms import MyUserCreationForm, MyUserUpdateForm
# Create your views here.


class UserProfileView(DetailView):
    template_name       = "users/user_profile.html"
    model               = get_user_model()
    context_object_name = "profile"
    slug_field          = "login"
    slug_url_kwarg      = "login"

    
@login_required
def my_profile(request):
    '''Shows logged user profile'''
    user = request.user
    context = {}
    return render(request, "users/user_profile.html", context)

def signup_view(request):
    '''View for creating new accounts'''
    if request.method == "GET":
        form = MyUserCreationForm()
        return render(request, "users/signup.html", {"form": form})
    else:
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save() #creates user
            data = form.cleaned_data
            user = authenticate(email = data["email"], password=data["password1"])    #there are password1 and password2, theyre the same if validation is ok
            login(request, user)
            return redirect(reverse("profile", args=(user.login,)))
    return render(request, "users/signup.html", {"form": form})

@login_required()
def edit_view(request):
    '''Proile edit view'''
    if request.method == "POST":
        form = MyUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            user = get_user(request)
            return redirect(reverse("profile", args=(user.login,)))
    else:
        form = MyUserUpdateForm(instance=request.user)
    
    context = {"form": form}
    return render(request, "users/user_profile_edit.html", context)

