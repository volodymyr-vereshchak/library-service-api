from rest_framework import serializers

from .models import Borrow
from book.serializers import BookSerializer
from book.models import Book
from .telegram import TelegramBot
from payment.payment import create_payment_session
from payment.models import Payment
from payment.serializers import PaymentSerializer
from django.db import transaction


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
            "payments"
        )
        read_only_fields = ["user", "actual_return_date", "payments"]

    @transaction.atomic
    def create(self, validated_data):
        book = Book.objects.get(id=validated_data["book"].id)
        if book.inventory > 0:            
            book.inventory -= 1
            book.save()            
            borrow = super().create(validated_data)
            create_payment_session(borrow, Payment.Type.PAYMENT)
            message = f"{validated_data['user'].first_name} {validated_data['user'].last_name} "\
            f"has successfuly borrowing '{book.title}' writting by {book.author} until {validated_data['expected_return_date']}"
            bot = TelegramBot()
            bot.send_message(message)
            return borrow
        raise serializers.ValidationError("No requested book in the library!")


class BorrowDetailSerializer(BorrowSerializer):
    book = BookSerializer(many=False, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
