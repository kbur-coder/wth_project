from rest_framework import serializers
from .models import Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'number', 'account_type', 'balance', 'currency', 'created_at', 'is_active']
        read_only_fields = ['id', 'number', 'balance', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'from_account', 'to_account', 'amount', 'timestamp', 'description']
        read_only_fields = ['id', 'timestamp']

class TransferSerializer(serializers.Serializer):
    from_account_id = serializers.IntegerField()
    to_account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    description = serializers.CharField(max_length=255, required=False)