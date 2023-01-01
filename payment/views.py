import stripe

from django.conf import settings
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .serializers import PaymentSerializer
from .models import Payment
from borrowing.telegram import TelegramBot


class PaymentView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_staff != True:
            return Payment.objects.filter(borrowing__user=current_user)
        return Payment.objects.all()

    @action(
        detail=False,
        methods=["GET"],
        url_path="success",
        permission_classes=[IsAuthenticated]
    )
    def success_url(self, request) -> None:
        stripe.api_key = settings.PAYMENT_SECRET_KEY
        session_id = request.GET.get('session_id')
        payment = Payment.objects.get(session_id=session_id)
        payment.status = Payment.Status.PAID
        payment.save()
        message = f"Transaction successfuly! Sum: {payment.money_to_pay}$"
        bot = TelegramBot()
        bot.send_message(message)
        return Response(data=f"Thanks, for your order!", status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        url_path="cancel",
        permission_classes=[IsAuthenticated]
    )
    def cancel_url(self, request) -> None:
        return Response(data="You can pay later, but the session is available for only 24h", status=status.HTTP_402_PAYMENT_REQUIRED)
