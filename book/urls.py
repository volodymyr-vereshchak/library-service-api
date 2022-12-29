from django.urls import path, include
from django.conf import settings

from rest_framework import routers

from .views import BookView

router = routers.SimpleRouter()
router.register("books", BookView)
