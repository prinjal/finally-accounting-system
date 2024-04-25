from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import AccountViewSet, TransactionViewSet, TransactionsByAccountView

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/transactions/<int:account_id>/', TransactionsByAccountView.as_view(), name='transactions-by-account'),
]
