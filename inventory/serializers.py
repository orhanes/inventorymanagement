from rest_framework import serializers
from .models import Stock, StockCard

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'name', 'serial_number']

class StockCardSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    class Meta:
        model = StockCard
        fields = ['id', 'stock', 'serial_number', 'lot', 'quantity', 'date', 'barcode', 'qr_code'] 