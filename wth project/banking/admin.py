from django.contrib import admin
from .models import Account, Transaction, Card

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('number', 'owner', 'account_type', 'balance', 'currency')
    list_filter = ('account_type', 'currency')
    search_fields = ('number', 'owner__username', 'owner__first_name', 'owner__last_name')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_account', 'to_account', 'amount', 'date')
    list_filter = ('date',)
    search_fields = ('from_account__number', 'to_account__number', 'description')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('number', 'card_type', 'account', 'owner_name', 'expiry_date', 'is_active')
    list_filter = ('card_type', 'is_active')
    search_fields = ('number', 'account__number', 'owner_name')