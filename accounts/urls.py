# accounts/urls.py

from django.urls import path, include
from rest_framework_nested import routers
from .views import AccountViewSet, LoginAPIView, TransactionViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)

accounts_router=routers.NestedDefaultRouter(router,r'accounts',lookup='account')
accounts_router.register(r'transactions',TransactionViewSet,basename='transactions-by-account')


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('', include(router.urls)),
    path('', include(accounts_router.urls)),
]
