from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Book
from .serializers import BookSerializer


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [
                AllowAny,
            ]
        return super().get_permissions()
