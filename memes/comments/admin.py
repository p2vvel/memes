from django.contrib import admin

# Register your models here.
from .models import MemeComment
from django.urls import reverse
from django.utils import safestring, html


class MemeCommentAdmin(admin.ModelAdmin):
    list_display = ("comment_object", "original_poster", "content", "is_reply", "karma", "hidden", "date_created")

    fields = (
        "original_poster", "content", "karma", "hidden", "parent_comment_content",
        "date_created", "date_edited", "meme", "comment_object")
    readonly_fields = (
        "meme", "parent_comment", "content", "original_poster", "parent_comment_content",
        "comment_object", "date_created", "date_edited")

    view_on_site = True
    save_on_top = True

    def get_view_on_site_url(self, comment: MemeComment) -> str:
        return reverse("meme_view", args=(comment.comment_object.pk,))

    def parent_comment_content(self, comment: MemeComment) -> safestring.SafeString:
        if comment.parent_comment:
            link = reverse("admin:comments_memecomment_change", args=(comment.parent_comment.pk,))
            return html.format_html(f'<a href="{link}">{comment.parent_comment.content}</a>')
        else:
            return safestring.SafeString('')

    parent_comment_content.allow_tags = True

    def is_reply(self, c: MemeComment) -> bool:
        return True if c.parent_comment else False

    is_reply.boolean = True

    def meme(self, c: MemeComment) -> safestring.SafeString:
        """Get html img tag with meme img as src"""
        return html.format_html(f'<img alt="{c.comment_object.title}" src="{c.comment_object.normal_image.url}">')

    meme.allow_tags = True


admin.site.register(MemeComment, MemeCommentAdmin)
