from yookassa import Payment, Configuration
import uuid
from .models import PaymentHistory, Organization, WebNotification


def payment_helper(request, total_price):
    Configuration.account_id = "some int here (acc number)"
    Configuration.secret_key = ""
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
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
    confirmation_url = payment.confirmation.confirmation_url
    return confirmation_url, payment.id


def check_payment(payment_history: PaymentHistory) -> bool:
    payment = Payment.find_one(payment_history.payment_id)
    if payment.paid:
        org = Organization.objects.get(user=payment_history.user)
        org.payment = True
        org.save()
        return True
    else:
        return False


def close_item_notifications(arg1, arg2=None):
    if arg2 is None:
        if isinstance(arg1, int):  # Only pk is provided
            filters = {'item_id': arg1}
        else:  # Only user is provided
            filters = {'user_id': arg1}
    else:
        filters = {'user_id': arg1, 'item_id': arg2}
    WebNotification.objects.filter(**filters).update(is_new=False)



