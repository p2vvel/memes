from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django import forms

# Register your models here.
from .models import MyUser

from django.utils import safestring
from django.utils import html
from django.urls import reverse

from memes_app.models import Meme


class AddMyUserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirm", widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ("email", "login", "password", "is_superuser")


class MemeInline(admin.TabularInline):
    model = Meme
    fields = ("title", "description", "category", "karma", "accepted", "hidden", "date_created")
    readonly_fields = fields
    show_change_link = True
    can_delete = False  # don't want to hide memes from admin panel
    ordering = ("-date_created",)

    def has_add_permission(self, request, obj=None):
        """Don't want to add memes from admin panel, no option for easier implementing it as in 'can_delete' """
        return False


class MyUserAdmin(UserAdmin):
    inlines = (MemeInline,)
    list_display = ("email", "login", "is_active", "is_superuser", "karma")
    readonly_fields = ("password", "date_created", "last_login", "get_avatar")

    add_fieldsets = (
        ("Info", {'fields': ('login', 'email', 'profile_img')}),
        ("Password", {"fields": ('password1', 'password2')}),
        ("Status", {'fields': ("is_superuser",), }))

    fieldsets = (
        ("Info", {'fields': ('login', 'email', 'profile_img', 'get_avatar')}),
        ("Status", {'fields': ('karma', 'is_superuser', 'is_active')}),)

    filter_horizontal = ()
    list_filter = ("is_active", "is_superuser")
    ordering = ()
    search_fields = ("login", "email")

    def get_avatar(self, user: MyUser) -> safestring.SafeString:
        """Returns html img tag with URL to users avatar as src value"""
        if user.profile_img:
            return html.format_html(f'<img alt="{user.login} avatar" src="{user.profile_img.url}">')
        else:
            return None

    get_avatar.allow_tags = True

    view_on_site = True
    save_on_top = True

    def get_view_on_site_url(self, user: MyUser) -> str:
        return reverse("profile", args=(user.login,))


admin.site.register(MyUser, MyUserAdmin)
