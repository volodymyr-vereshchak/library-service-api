from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Borrow
from .serializers import BorrowSerializer, BorrowListSerializer


class BorrowView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [
        IsAuthenticated,
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowListSerializer
        return BorrowSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_staff != True:
            return Borrow.objects.filter(user=current_user)
        return Borrow.objects.all()
