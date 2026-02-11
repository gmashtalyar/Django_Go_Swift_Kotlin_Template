from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from typing import Callable, List, Any, Optional
from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps


def allowed_users(allowed_roles: Optional[List[str]] = None) -> Callable[[Callable[..., HttpResponse]], Callable[..., HttpResponse]]:
    """
    Decorator for views that checks if the user is logged in AND has a specific role.
    Redirects to 'login' if not authenticated.
    Returns 403 Forbidden if authenticated but wrong role.
    """
    def decorator(view_func: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
        @wraps(view_func)
        def wrapper_func(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            roles = allowed_roles or []
            if not request.user.is_authenticated:
                login_url = reverse("users:login")
                return redirect(f"{login_url}?next={request.get_full_path()}")
            user_groups: List[str] = []
            if request.user.groups.all():
                user_groups = [group.name for group in request.user.groups.all()]
            if any(role in roles for role in user_groups):
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
