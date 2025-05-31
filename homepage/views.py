from django.shortcuts import render
from django.views.generic import View, TemplateView
from inventory.models import Stock
from transactions.models import SaleBill, PurchaseBill
from transactions.models import Buyer
from transactions.models import Supplier
import json


class HomeView(View):
    template_name = "home.html"
    def get(self, request):        
        # Grafik verileri
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
        labels = [item.name for item in stockqueryset]
        data = [item.quantity for item in stockqueryset]
        
        # Son işlemler
        sales = SaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        
        # İstatistik verileri
        total_products = Stock.objects.filter(is_deleted=False).count()
        total_customers = Buyer.objects.count()
        total_suppliers = Supplier.objects.count()
        total_sales = SaleBill.objects.count()
        
        context = {
            'labels': json.dumps(labels),
            'data': json.dumps(data),
            'sales': sales,
            'purchases': purchases,
            'total_products': total_products,
            'total_customers': total_customers,
            'total_suppliers': total_suppliers,
            'total_sales': total_sales
        }
        return render(request, self.template_name, context)

class AboutView(TemplateView):
    template_name = "about.html"