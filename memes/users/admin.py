from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django import forms

# Register your models here.
from .models import MyUser


class AddMyUserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confim", widget=forms.PasswordInput)
    
    class Meta:
        model = MyUser
        fields = ("email", "login", "password", "is_superuser")


class MyUserAdmin(UserAdmin):
    list_display = ("email", "login", "is_active", "is_superuser", "karma")
    readonly_fields = ("password", "date_created", "last_login")

    add_fieldsets = (
                ("Info", {'fields': ('login', 'email')}), 
                ("Password", {"fields": ('password1', 'password2')}),
                ("Status", {'fields': ("is_superuser",)}) )
    
    fieldsets = (
                ("Info", {'fields': ('login', 'email',)}),
                ("Status", {'fields': ('karma', 'is_superuser', 'is_active')}),)
    
    filter_horizontal = ()
    list_filter = ()
    ordering = ()
    search_fields = ("login", "email")
    # add_form = AddMyUserForm

admin.site.register(MyUser, MyUserAdmin)