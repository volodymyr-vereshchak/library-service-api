from django.urls import path, include

from rest_framework import routers

from .views import BookView

app_name = "book"

router = routers.DefaultRouter()
router.register("books", BookView)

urlpatterns = [
    path("", include(router.urls))
]
