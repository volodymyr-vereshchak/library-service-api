from rest_framework import routers

from .views import PaymentView

router = routers.SimpleRouter()
router.register("payments", PaymentView)
