from rest_framework import serializers

from .models import Borrow
from book.serializers import BookSerializer
from book.models import Book


class BorrowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(many=False, read_only=True, slug_field="email")

    class Meta:
        model = Borrow
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
        read_only_fields = ["user", "actual_return_date"]

    def create(self, validated_data):
        book = Book.objects.get(id=validated_data["book"].id)
        if book.inventory > 0:
            book.inventory -= 1
            book.save()
            return super().create(validated_data)
        raise serializers.ValidationError("No requested book in the library!")


class BorrowListSerializer(BorrowSerializer):
    book = BookSerializer(many=False, read_only=True)