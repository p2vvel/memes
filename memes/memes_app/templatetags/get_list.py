from django import template

register = template.Library()


@register.filter
def get_list(data, index):
    """Returns list of elements at given index"""
    return data.getlist(index)  #no need to check existence, non-existing index will return []

