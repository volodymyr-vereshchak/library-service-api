from rest_framework import serializers

from .models import Borrow
from book.serializers import BookSerializer
from book.models import Book
from .telegram import TelegramBot


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
            message = f"{validated_data['user'].first_name} {validated_data['user'].last_name} "\
            f"has successfuly borrowing '{book.title}' writting by {book.author} until {validated_data['expected_return_date']}"
            bot = TelegramBot()
            bot.send_message(message)
            return super().create(validated_data)
        raise serializers.ValidationError("No requested book in the library!")


class BorrowListSerializer(BorrowSerializer):
    book = BookSerializer(many=False, read_only=True)