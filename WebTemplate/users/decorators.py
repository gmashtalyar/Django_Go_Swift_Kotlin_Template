from typing import Callable, List, Any
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps


def allowed_users(allowed_roles: List[str] = []) -> Callable[[Callable[..., HttpResponse]], Callable[..., HttpResponse]]:
    """
    Decorator for views that checks if the user is logged in AND has a specific role.
    Redirects to 'login' if not authenticated.
    Returns 403 Forbidden if authenticated but wrong role.
    """
    def decorator(view_func: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
        @wraps(view_func)
        def wrapper_func(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            if not request.user.is_authenticated:
                return redirect('login')
            user_groups: List[str] = []
            if request.user.groups.all():
                user_groups = [group.name for group in request.user.groups.all()]
            if any(role in allowed_roles for role in user_groups):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("У вас нет доступа к этой странице")
        return wrapper_func
    return decorator


def organization_payment_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        from .models import Organization
        if not request.user.is_authenticated:
            return redirect('users:org-registration-process-info')
        try:
            organization = Organization.objects.get(user=request.user)
            if not organization.payment:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('users:org-registration-process-info')
        except Organization.DoesNotExist:
            return redirect('users:org-registration-process-info')
    return _wrapped_view
