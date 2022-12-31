import stripe
from decimal import Decimal

from datetime import date
from django.conf import settings
from borrowing.models import Borrow
from .models import Payment

def calculate_payment(expected_return_date: date, actual_return_date: date, daily_fee: Decimal, type: Payment.Type) -> Decimal:
    if type == Payment.Type.PAYMENT:
        delta = expected_return_date - date.today()
        return Decimal(daily_fee * Decimal(delta.days))
    delta = actual_return_date - expected_return_date
    return Decimal(daily_fee * Decimal(delta.days) * settings.FINE_MULTIPLIER)

def create_payment_session(borrow: Borrow, type: Payment.Type):
    stripe.api_key = settings.PAYMENT_SECRET_KEY
    money_to_pay = calculate_payment(borrow.expected_return_date, borrow.actual_return_date, borrow.book.daily_fee, type)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                'name': f'{borrow.book.title}',
                },
                'unit_amount': int(money_to_pay) * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/payments/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://localhost/payments/cancel',
    )
    
    Payment.objects.create(
        status=Payment.Status.PENDING,
        type=type,
        borrowing=borrow,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=money_to_pay
    )
