# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, TransactionViewSet, TransactionsByAccountView

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('transactions/<int:account_id>/', TransactionsByAccountView.as_view(), name='transactions-by-account'),
    path('', include(router.urls)),
]
