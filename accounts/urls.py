# accounts/urls.py

from django.urls import path, include
from rest_framework_nested import routers
from .views import AccountViewSet, TransactionViewSet

router = routers.DefaultRouter()
router.register(r'accounts', AccountViewSet)

accounts_router=routers.NestedDefaultRouter(router,r'accounts',lookup='account')
accounts_router.register(r'transactions',TransactionViewSet,basename='transactions-by-account')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(accounts_router.urls)),
]
