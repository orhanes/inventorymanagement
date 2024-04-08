import django_filters
from .models import Buyer, Supplier, Delivery, Receipt, MailOrder    

class BuyerFilter(django_filters.FilterSet):                            # Müşteri adıyla arama filtresi
    name = django_filters.CharFilter(lookup_expr='icontains')           # Tüm ad girilmese de aramayı yapar
    class Meta:
        model = Buyer
        fields = ['name']

class SupplierFilter(django_filters.FilterSet):                         # Tedarikçi adıyla arama filtresi
    name = django_filters.CharFilter(lookup_expr='icontains')           # Tüm ad girilmese de aramayı yapar
    class Meta:
        model = Supplier
        fields = ['name']

class DeliveryFilter(django_filters.FilterSet):                         # Şoför adıyla arama filtresi
    name = django_filters.CharFilter(lookup_expr='icontains')           # Tüm ad girilmese de aramayı yapar
    class Meta:
        model = Delivery
        fields = ['courier_name']

class ReceiptFilter(django_filters.FilterSet):                         # Müşteri adıyla arama filtresi
    name = django_filters.CharFilter(lookup_expr='icontains')           # Tüm ad girilmese de aramayı yapar
    class Meta:
        model = Receipt
        fields = ['buyer']

class MailOrderFilter(django_filters.FilterSet):                         # Müşteri adıyla arama filtresi
    name = django_filters.CharFilter(lookup_expr='icontains')           # Tüm ad girilmese de aramayı yapar
    class Meta:
        model = MailOrder
        fields = ['customer_name']