"""memes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import UserProfileView, edit_view, signup_view
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("signup/", signup_view, name="signup"),
    # path("profile/", my_profile, name="my_profile"),
    path("profile/<slug:login>/", UserProfileView.as_view(), name="profile"),
    
    path("profile_edit/", edit_view, name="profile_edit"),
    path("login/", auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name="users/login.html"), name="login"),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="users/password_change_form.html"), name="password_change"),
    path("password_change_done/", auth_views.PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name="password_change_done"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
