from django.urls import path, include

from rest_framework import routers

from .views import BorrowView

app_name = "borrow"

router = routers.DefaultRouter()
router.register("borrowings", BorrowView)

urlpatterns = [path("", include(router.urls))]
