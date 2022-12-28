from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Borrow
from .serializers import BorrowSerializer


class BorrowView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]
