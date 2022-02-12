from .models import Category


def available_categories(request):
    """Add list of available categories to every template"""
    if request.user.is_authenticated:
        return {"available_categories": Category.objects.all().order_by("name")}
    else:
        return {"available_categories": Category.objects.filter(public=True).order_by("public", "name")}
