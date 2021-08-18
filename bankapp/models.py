from django.db import models
from django.utils import timezone

# Create your models here.

class Customer(models.Model):
    account_number = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    balance = models.PositiveBigIntegerField()

    def __str__(self):
        return str(self.account_number)

class Transaction(models.Model):
    account_number = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transacted_amount = models.PositiveBigIntegerField()
    time = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=10)

    def __str__(self):
        return str(self.time)
