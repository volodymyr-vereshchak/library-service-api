from django.db import models

from borrowing.models import Borrow

class Payment(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 0
        PAID = 1
    
    class Type(models.IntegerChoices):
        PAYMENT = 0
        FINE = 1
    
    status = models.BooleanField(choices=Status.choices)
    type = models.BooleanField(choices=Type.choices)
    borrowing = models.ForeignKey(Borrow, on_delete=models.CASCADE, related_name="payments")
    session_url = models.URLField(max_length=512)
    session_id = models.CharField(max_length=255, unique=True)
    money_to_pay = models.DecimalField(max_digits=8, decimal_places=2)
