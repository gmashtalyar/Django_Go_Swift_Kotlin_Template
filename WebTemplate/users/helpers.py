from typing import Optional, Union, Tuple, Any
from yookassa import Payment, Configuration
import uuid
from .models import PaymentHistory, Organization, WebNotification


def payment_helper(request: Any, total_price: Union[int, float, str]) -> Tuple[str, str]:
    # TODO: request type should be HttpRequest from django.http, but using Any to avoid import
    Configuration.account_id = "some int here (acc number)"
    Configuration.secret_key = ""
    idempotence_key: str = str(uuid.uuid4())
    payment: Payment = Payment.create({
        "amount": {
            "value": f"{total_price}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"",
        },
        "metadata": {
            "user_id": request.user.id,
            "payment": f"{total_price}"
        },
        "test": True,
        "capture": True,
        "description": "Оплата XXXXXXXX"
    }, idempotence_key)
    confirmation_url: str = payment.confirmation.confirmation_url
    return confirmation_url, payment.id


def check_payment(payment_history: PaymentHistory) -> bool:
    payment: Payment = Payment.find_one(payment_history.payment_id)
    if payment.paid:
        org: Organization = Organization.objects.get(user=payment_history.user)
        org.payment = True
        org.save()
        return True
    else:
        return False


def close_item_notifications(arg1: Union[int, Any], arg2: Optional[int] = None) -> None:
    # TODO: arg1 can be int (item_id) or User model instance (user), consider using overload or better naming
    filters: dict[str, Union[int, Any]]
    if arg2 is None:
        if isinstance(arg1, int):  # Only pk is provided
            filters = {'item_id': arg1}
        else:  # Only user is provided
            filters = {'user_id': arg1}
    else:
        filters = {'user_id': arg1, 'item_id': arg2}
    WebNotification.objects.filter(**filters).update(is_new=False)



