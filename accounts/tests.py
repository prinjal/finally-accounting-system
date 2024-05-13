from django.test import TestCase
from .models import Account, Transaction
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import AccountSerializer, TransactionSerializer

class ViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test", password="test")
        self.account = Account.objects.create(account_number="1234567890123456", current_balance=1000.00, user=self.user)
        self.transaction = Transaction.objects.create(date='2023-04-01', transaction_type='CREDIT', note='Initial deposit', amount=1000.00, account=self.account)

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_transactions_by_account(self):
        url = reverse('transaction-list')
        response = self.client.get(url, {'account_pk': self.account.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transactions = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(transactions), 6)

    def test_create_transaction(self):
        url = reverse('transactions-by-account-list', kwargs={'account_pk': self.account.id})
        transaction_data = {
            'date': '2023-04-02',
            'transaction_type': 'DEBIT',
            'note': 'Purchase',
            'amount': 200.00
        }
        response = self.client.post(url, transaction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.account.refresh_from_db()
        self.assertEqual(self.account.current_balance, 800.00)

class SerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.account_attributes = {'account_number': "1234567890123456", 'current_balance': 1000.00, 'user': self.user}
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
        self.user = User.objects.create_user(username="test", password="test")
        self.account = Account.objects.create(account_number="9876543210123456", current_balance=500.00, user=self.user)

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_transaction_effect_on_balance(self):
        transaction_data = {
            'date': '2023-04-01',
            'transaction_type': 'DEBIT',
            'note': 'Withdrawal',
            'amount': 200.00
        }

        context = {'account_id': self.account.id}
        serializer = TransactionSerializer(data=transaction_data, context=context)
        if serializer.is_valid():
            serializer.save()

        self.account.refresh_from_db()
        self.assertEqual(self.account.current_balance, 300.00)

    def test_transaction_creation_with_serializer(self):
        transaction_data = {
            'date': '2023-04-01',
            'transaction_type': 'CREDIT',
            'note': 'Deposit',
            'amount': 100.00
        }

        context = {'account_id': self.account.id}
        serializer = TransactionSerializer(data=transaction_data, context=context)
        if serializer.is_valid():
            transaction = serializer.save()

        self.assertTrue(serializer.is_valid())
        self.assertEqual(transaction.amount, 100.00)
        self.assertEqual(transaction.account_id, self.account.id)

        self.account.refresh_from_db()
        self.assertEqual(self.account.current_balance, 600.00)
