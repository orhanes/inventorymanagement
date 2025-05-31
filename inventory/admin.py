from django.contrib import admin
from .models import Stock, StockCard, StockLog

admin.site.register(Stock)
admin.site.register(StockCard)
admin.site.register(StockLog)