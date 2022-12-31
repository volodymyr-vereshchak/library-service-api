from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated


from .serializers import PaymentSerializer
from .models import Payment


class PaymentView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_staff != True:
            return Payment.objects.filter(borrowing__user=current_user)
        return Payment.objects.all()
