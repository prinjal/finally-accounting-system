from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer, UserSerializer
from django.db.models import Sum, Q
from rest_framework.decorators import action
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        if 'account_pk' in self.kwargs:
            return Transaction.objects.filter(account_id=self.kwargs['account_pk'])
        else:
            return Transaction.objects.all()

    def get_serializer_context(self):
        if 'account_pk' in self.kwargs:
            return {'account_id':self.kwargs['account_pk']}
    

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @action(detail=True, methods=['get'])
    def balance_on_date(self, request, pk=None):
        account = self.get_object()
        date = request.query_params.get('date', None)
        
        if date is not None:
            # Calculate the sum of credits up to the date
            credits = account.transactions.filter(
                transaction_type='CREDIT', date__gte=date
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            # Calculate the sum of debits up to the date
            debits = account.transactions.filter(
                transaction_type='DEBIT', date__lte=date
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            # Starting balance + credits - debits
            balance_on_date = account.current_balance + credits - debits
            return Response({'balance_on_date': balance_on_date})
        else:
            return Response({'error': 'Date parameter is required.'}, status=400)

