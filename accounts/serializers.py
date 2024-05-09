from rest_framework import serializers
from .models import Transaction, Account
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_number', 'current_balance', 'user']

class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'transaction_type', 'note', 'amount', 'account']
    
    def create(self, validated_data):
        account_id=self.context.get('account_id')
        account = Account.objects.get(pk=account_id)
        
        transaction = Transaction.objects.create(account=account, **validated_data)

        # Update the account's balance based on the transaction type
        if validated_data['transaction_type'] == 'CREDIT':
            account.current_balance += validated_data['amount']
        elif validated_data['transaction_type'] == 'DEBIT':
            account.current_balance -= validated_data['amount']
        account.save()

        return transaction
