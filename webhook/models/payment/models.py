from django.db import models

class PaymentType(models.TextChoices):
    PAYMENT = 'PAYMENT', 'Payment'
    FUNDING = 'FUNDING', 'Funding'
    COMPENSATION = 'COMPENSATION', 'Compensation'

class AddBalance(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=64, choices=PaymentType.choices)
    source = models.CharField(max_length=1024)