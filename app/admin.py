from django.contrib import admin
from app.models import *
# Register your models here.
admin.site.register(User)
admin.site.register(LimitOrder)
admin.site.register(CurrentMarketPrice)
admin.site.register(TradeHistory)
