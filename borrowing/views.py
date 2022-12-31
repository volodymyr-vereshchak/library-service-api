import datetime
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Borrow
from .serializers import BorrowSerializer, BorrowDetailSerializer
from book.models import Book
from payment.payment import create_payment_session
from payment.models import Payment
from django.db import transaction
from .filters import BorrowFilter, BorrowFilterAdmin


class BorrowView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [
        IsAuthenticated,
    ]
    filterset_class = BorrowFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowDetailSerializer
        return BorrowSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_staff != True:
            return Borrow.objects.filter(user=current_user)
        self.filterset_class = BorrowFilterAdmin
        return Borrow.objects.all()

    @transaction.atomic
    @action(
        detail=True,
        methods=["GET"],
        url_path="return",
        permission_classes=[IsAuthenticated]
    )    
    def return_book(self, request, pk: int) -> None:
        borrow = self.get_object()
        if borrow.actual_return_date is None and borrow:
            borrow.actual_return_date = datetime.date.today()
            borrow.save()
            book = Book.objects.get(id=borrow.book.id)
            book.inventory += 1
            book.save()
            delta = datetime.date.today() - borrow.expected_return_date
            if delta.days > 0:
                create_payment_session(borrow, Payment.Type.FINE)
                return Response(data="You have to pay fine payment!", status=status.HTTP_402_PAYMENT_REQUIRED)
            return Response(status=status.HTTP_200_OK)
        return Response(data="You can't return this book!", status=status.HTTP_400_BAD_REQUEST)
