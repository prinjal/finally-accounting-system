from django.test import TestCase

from accounts.serializers import AccountSerializer, TransactionSerializer
from .models import Account, Transaction
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

class ViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.account = Account.objects.create(account_number="1234567890123456", current_balance=1000.00, user=100)
        self.transaction = Transaction.objects.create(date='2023-04-01', transaction_type='CREDIT', note='Initial deposit', amount=1000.00, account=self.account)

    def test_get_transactions_by_account(self):
        url = reverse('transactions-by-account', kwargs={'account_id': self.account.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Checking if one transaction is returned


class ModelTestCase(TestCase):
    def setUp(self):
        self.account = Account.objects.create(account_number="1234567890123456", current_balance=1000.00, user=100)

    def test_account_creation(self):
        self.assertIsInstance(self.account, Account)
        self.assertEqual(self.account.account_number, "1234567890123456")
        self.assertEqual(self.account.current_balance, 1000.00)

class SerializerTestCase(TestCase):
    def setUp(self):
        self.account_attributes = {'account_number': "1234567890123456", 'current_balance': 1000.00, 'user': 100}
        self.account = Account.objects.create(**self.account_attributes)
        self.serializer = AccountSerializer(instance=self.account)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'account_number', 'current_balance', 'user']))

    def test_account_data(self):
        data = self.serializer.data
        self.assertEqual(data['account_number'], self.account_attributes['account_number'])


class IntegrationTestCase(TestCase):
    def setUp(self):
        self.account = Account.objects.create(account_number="9876543210123456", current_balance=500.00, user=100)

    def test_transaction_effect_on_balance(self):
        # Create the transaction data dictionary
        transaction_data = {
            'date': '2023-04-01',
            'transaction_type': 'DEBIT',
            'note': 'Withdrawal',
            'amount': 200.00,
            'account_id': self.account.id  # Passing account ID to the serializer
        }

        # Use TransactionSerializer to create the transaction
        serializer = TransactionSerializer(data=transaction_data)
        if serializer.is_valid():
            serializer.save()

        # Refresh account from DB to get updated balance
        self.account.refresh_from_db()

        # Assert the account's balance has been updated
        self.assertEqual(self.account.current_balance, 300.00)

    def test_transaction_creation_with_serializer(self):
        # Ensure transaction is created correctly with serializer
        transaction_data = {
            'date': '2023-04-01',
            'transaction_type': 'CREDIT',
            'note': 'Deposit',
            'amount': 100.00,
            'account_id': self.account.id
        }

        # Instantiate serializer with data
        serializer = TransactionSerializer(data=transaction_data)
        if serializer.is_valid():
            transaction = serializer.save()

        # Validate response
        self.assertTrue(serializer.is_valid())
        self.assertEqual(transaction.amount, 100.00)
        self.assertEqual(transaction.account_id, self.account.id)

        # Recheck the balance
        self.account.refresh_from_db()
        self.assertEqual(self.account.current_balance, 600.00)  # Initial 500 + 100 credit

