from rest_framework import routers

from .views import BookView

router = routers.SimpleRouter()
router.register("books", BookView)
