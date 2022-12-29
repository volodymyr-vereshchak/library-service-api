import datetime
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Borrow
from .serializers import BorrowSerializer, BorrowListSerializer
from book.models import Book


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
        if self.action == "retrieve":
            return BorrowListSerializer
        return BorrowSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_staff != True:
            return Borrow.objects.filter(user=current_user)
        return Borrow.objects.all()

    @action(
        detail=True,
        methods=["GET"],
        url_path="return",
        permission_classes=[IsAuthenticated]
    )
    def return_book(self, request, pk: int) -> None:
        borrow = self.get_object()
        if borrow.actual_return_date is None and borrow:
            borrow.actual_return_date = datetime.datetime.now().date
            borrow.save()
            book = Book.objects.get(id=borrow.book.id)
            book.inventory += 1
            book.save()
            return Response(status=status.HTTP_200_OK)
        return Response(data="You can't return this book!", status=status.HTTP_400_BAD_REQUEST)
