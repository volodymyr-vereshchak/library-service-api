from django.urls import path, include

from rest_framework import routers

from .views import BorrowView

router = routers.SimpleRouter()
router.register("borrowings", BorrowView, basename="borrow")
