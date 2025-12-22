from typing import Optional

from django.http import HttpRequest


def get_user_id(request: HttpRequest) -> Optional[int]:
    return request.user.id