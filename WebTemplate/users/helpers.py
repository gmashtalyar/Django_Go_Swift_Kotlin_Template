from yookassa import Payment, Configuration
import uuid
from .models import PaymentHistory, Organization


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
