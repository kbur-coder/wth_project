from django.db import models

# Create your models here.
from accounts.models import User
from django.core.validators import MinValueValidator


class Account(models.Model):
    ACCOUNT_TYPES = (
        ('checking', 'Checking'),
        ('savings', 'Savings'),
        ('credit', 'Credit'),
        ('deposit', 'Deposit'),
    )

    CURRENCIES = (
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('SUM', 'Uzbek Sum'),
    )

    number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    opened_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.number} ({self.get_account_type_display()})"


class Transaction(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='outgoing_transactions')
    to_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='incoming_transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Transaction #{self.id}"


class Card(models.Model):
    CARD_TYPES = (
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    )

    number = models.CharField(max_length=16, unique=True)
    card_type = models.CharField(max_length=6, choices=CARD_TYPES)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='cards')
    owner_name = models.CharField(max_length=100)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)
    issued_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Card {self.number}"


