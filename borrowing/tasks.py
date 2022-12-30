from datetime import date, timedelta
from celery import shared_task

from borrowing.models import Borrow
from book.models import Book
from user.models import User
from .telegram import TelegramBot

TOMORROW = tomorrow = date.today() + timedelta(days=1)

def check_overdue() -> list:
    overdue = Borrow.objects.filter(expected_return_date__lte=TOMORROW).values("book", "user", "expected_return_date")
    return overdue

def send_notification(message: str) -> None:
    bot = TelegramBot()
    bot.send_message(message)

@shared_task
def overdue_notification() -> None:
    overdue = check_overdue()
    if overdue:
        for borrow in overdue:
            days_overdue = TOMORROW - borrow["expected_return_date"]
            book = Book.objects.get(id=borrow["book"])
            user = User.objects.get(id=borrow["user"])
            message = f"{user.first_name} {user.last_name} has overdue {book.title} for {days_overdue}!"
            send_notification(message)
    else:
        message = "No borrowings overdue today!"
        send_notification(message)
