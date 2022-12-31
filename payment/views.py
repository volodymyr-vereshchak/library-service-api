from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser


from .serializers import PaymentSerializer
from .models import Payment


class PaymentView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]
