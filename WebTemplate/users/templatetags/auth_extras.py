from django import template
from django.contrib.auth.models import Group
from datetime import date

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter(name='has_any_group')
def has_any_group(user, group_names):
    group_names_list = group_names.split(',')
    groups = Group.objects.filter(name__in=group_names_list)
    return groups.exists() and user.groups.filter(pk__in=groups).exists()
