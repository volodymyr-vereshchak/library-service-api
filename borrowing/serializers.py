from rest_framework import serializers

from .models import Borrow
from book.serializers import BookSerializer
from book.models import Book
from .telegram import TelegramBot
from payment.payment import create_payment_session
from payment.models import Payment
from payment.serializers import PaymentSerializer
from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import date


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
        user = validated_data['user']
        pending_payments = Payment.objects.filter(borrowing__user=user, status=0).count()
        if pending_payments > 0:
            raise serializers.ValidationError("You have pending payments already!")
        book = Book.objects.get(id=validated_data["book"].id)
        if book.inventory > 0:            
            book.inventory -= 1
            book.save()            
            borrow = super().create(validated_data)
            request = self.context["request"]
            create_payment_session(borrow, Payment.Type.PAYMENT, request)
            message = f"{user.first_name} {user.last_name} "\
            f"has successfuly borrowing '{book.title}' writting by {book.author} until {validated_data['expected_return_date']}"
            bot = TelegramBot()
            bot.send_message(message)
            return borrow
        raise serializers.ValidationError("No requested book in the library!")

    def validate(self, attrs):
        if attrs["expected_return_date"] < date.today():
            raise ValidationError("Return date can't be less then today date!")
        return super().validate(attrs)


class BorrowDetailSerializer(BorrowSerializer):
    book = BookSerializer(many=False, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
