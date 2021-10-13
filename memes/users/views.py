from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required

from users.forms import MyUserCreationForm
# Create your views here.


class UserProfileView(DetailView):
    template_name = "users/user_profile.html"
    model = get_user_model()
    
@login_required
def my_profile(request):
    '''Shows logged logged user profile'''
    user = request.user
    context = {}
    return render(request, "users/user_profile.html", context)

def signup_view(request):
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
            return redirect("my_profile")
    return render(request, "users/signup.html", {"form": form})
        

