from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from django.db.models import Sum, Q
from rest_framework.decorators import action

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionsByAccountView(APIView):
    def get(self, request, account_id):
        transactions = Transaction.objects.filter(account__id=account_id)
        serializer = TransactionSerializer(transactions, many=True)
        print(serializer.data)
        return Response(serializer.data)
    

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

