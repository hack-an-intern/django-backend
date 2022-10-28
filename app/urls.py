from django.urls import path
from django.urls import include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tradehistory', TradeHistoryViewSet, basename='tradehistory')
router.register(r'price', CurrentMarketOrderViewSet, basename='price')
router.register(r'limitorder', LimitOrderViewSet, basename='limitorder')
urlpatterns = router.urls
urlpatterns += [
    path('trade', Trade.as_view(), name='trade')]
