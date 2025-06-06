from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group2 = []
            if request.user.groups.exists():
                group2 = [group.name for group in request.user.groups.all()]
            if any(x in allowed_roles for x in group2):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("У вас нет доступа к этой странице")  # return redirect("users:ask-signup")
        return wrapper_func
    return decorator


def organization_payment_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        from .models import Organization
        try:
            organization = Organization.objects.get(user=request.user)
            if not organization.payment:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('users:org-registration-process-info')
        except Organization.DoesNotExist:
            return redirect('users:org-registration-process-info')
    return _wrapped_view
