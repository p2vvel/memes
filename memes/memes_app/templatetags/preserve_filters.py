from django import template

register = template.Library()


@register.filter
def preserve_filters(url, url_params):
    """Adds my filters data to URLs (sort method and categories)"""
    result = "?"
    sort_method = url_params.get("sort", None)      # sort method info
    if sort_method:
        result += f"sort={sort_method}&"
    categories = url_params.getlist("category")     # categories data
    for c in categories:
        result += f"category={c}&"

    if result[-1] == "&" or result[-1] == "?":
        result = result[:-1]        # cut last character
    # TODO: fix issue with parameters disappearing at page change

    return url + result
