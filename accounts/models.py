from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    account_number = models.CharField(max_length=16, unique=True)
    current_balance = models.DecimalField(max_digits=14, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('CREDIT', 'Credit'),
        ('DEBIT', 'Debit'),
    ]
    date = models.DateField()
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE_CHOICES)
    note = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
