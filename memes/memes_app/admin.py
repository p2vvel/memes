from django.contrib import admin
from .models import Category, Meme, MemeKarma
from django.utils import html, safestring
from django.urls import reverse

from comments.models import MemeComment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "public"]


class MemeCommentsInline(admin.TabularInline):
    model = MemeComment
    fields = ("original_poster", "content", "karma", "hidden", "date_created")
    readonly_fields = ("original_poster", "content", "karma", "date_created")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        """Don't want to add memes from admin panel, no option for easier implementing it as in 'can_delete' """
        return False


class MemeAdmin(admin.ModelAdmin):
    list_display = ("meme", "title", "karma", "comments_count", "accepted", "hidden", "category", "original_poster")
    list_filter = ("accepted", "hidden", "date_created", "date_accepted", "category")
    list_editable = ("accepted", "hidden")
    sortable_by = ("date_created", "date_accepted", "karma")
    ordering = ["-date_created", "-date_accepted"]

    fields = (
        "hidden", "accepted", "title", "meme", "description", "karma", "comments_count", "original_poster",
        "date_created", "date_accepted", "original_image", "normal_image")

    readonly_fields = ("meme", "original_poster", "date_created", "original_image", "normal_image", "comments_count")
    search_fields = ("title", "description", "original_poster__login", "original_poster__email")
    inlines = (MemeCommentsInline,)

    view_on_site = True
    save_on_top = True

    def meme(self, m: Meme) -> safestring.SafeString:
        """Get html img tag with meme img as src"""
        return html.format_html(f'<img alt="{m.title}" src="{m.normal_image.url}">')

    meme.allow_tags = True

    def get_view_on_site_url(self, m: Meme) -> str:
        if m:
            return reverse("meme_view", args=(m.pk,))
        else:
            return ''


admin.site.register(Meme, MemeAdmin)
admin.site.register(Category, CategoryAdmin)
