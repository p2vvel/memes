from logging import log
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, get_user, get_user_model, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.http import Http404

from users.forms import MyUserCreationForm, MyUserUpdateForm
from .models import Karma
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




#signed in users wont see sign up view
@user_passes_test(lambda user: user.is_anonymous, redirect_field_name="index")
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


def user_karma_change(request, login):
    if request.user.is_authenticated:
        MyUserModel = get_user_model()
        sender = get_user(request)
    
        recipient = get_object_or_404(klass=MyUserModel, login=login)

        #NO CHEATING
        #TODO: give some information after such incident
        if recipient == sender:
            return redirect("index")

        try:
            given_karma = Karma.objects.get(sender=sender, recipient=recipient) #recipient was previously given karma point by sender
            given_karma.delete()
            recipient.karma -= 1
            recipient.save()
        except Karma.DoesNotExist:
            #recipient wasnt given karma point by sender
            karma = Karma(sender=sender, recipient=recipient)
            karma.save()
            recipient.karma += 1
            recipient.save()
        
        return redirect(reverse("profile", args=(recipient.login,)))
    else:
        return redirect("index")

