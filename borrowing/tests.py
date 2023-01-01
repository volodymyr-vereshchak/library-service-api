from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta
from book.models import Book

BORROW_URL = reverse("borrow-list")

def create_book() -> Book:
    data = {
        "title": "test_title",
        "author": "test_author",
        "cover": 0,
        "inventory": 5,
        "daily_fee": Decimal(10),
    }
    return Book.objects.create(**data)


class AnonTestBorrowView(APITestCase):
    def test_list_view(self):
        response = self.client.get(BORROW_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BorrowCreateTest(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test@test.com", "testpass", is_staff=False
        )
        self.client.force_authenticate(self.user)

    def test_book_inventory(self) -> None:
        book = create_book()
        return_date = date.today() + timedelta(days=10)
        data = {
            "expected_return_date": return_date,
            "book": book.id
        }
        response = self.client.post(BORROW_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(id = book.id)
        self.assertEqual(book.inventory, 4)

    def test_return_book(self) -> None:
        book = create_book()
        return_date = date.today() + timedelta(days=10)
        data = {
            "expected_return_date": return_date,
            "book": book.id
        }
        response = self.client.post(BORROW_URL, data=data)
        return_url = reverse("borrow-detail", kwargs={"pk": response.data["id"]}) + "return/"
        response = self.client.get(return_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = Book.objects.get(id = book.id)
        self.assertEqual(book.inventory, 5)
