from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
        # return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group2 = []
            if request.user.groups.exists():
                group2 = [group.name for group in request.user.groups.all()]
            if any(x in allowed_roles for x in group2):
                return view_func(request, *args, **kwargs)
            else:
                return redirect("users:ask-signup")
        return wrapper_func
    return decorator
