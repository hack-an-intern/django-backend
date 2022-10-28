from django.urls import path
from django.urls import include
from app import views
from .views_market import *
user_patterns = [
    path('create/', views.create, name='create'),
    path('portfolio/<int:pk>', views.portfolio, name='portfolio'),
]
market_patterns = [
    path('price/', marketprice, name='price'),
    path('orderbook/', orderbook, name='orderbook'),
    path('tradehistory/', tradehistory, name='tradehistory'),
    path('trade/', trade, name='trade'),
]
urlpatterns = [
    path('', views.index, name='index'),
    path('user/', include(user_patterns)),
    path('market/', include(market_patterns)),
]

