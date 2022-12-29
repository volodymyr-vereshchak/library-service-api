from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Book
from .serializers import BookSerializer


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        self.permission_classes = (
            [
                AllowAny,
            ]
            if self.request.method == "GET"
            else [
                IsAdminUser,
            ]
        )
        return super().get_permissions()
