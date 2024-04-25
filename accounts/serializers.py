from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_number', 'current_balance', 'user']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'date', 'transaction_type', 'note', 'amount', 'account']
    def create(self, validated_data):
        transaction_type = validated_data.get('transaction_type')
        amount = validated_data.get('amount')
        account = validated_data.get('account')

        if transaction_type == 'CREDIT':
            account.current_balance += amount
        elif transaction_type == 'DEBIT':
            account.current_balance -= amount

        account.save()
        transaction = Transaction.objects.create(**validated_data)
        return transaction