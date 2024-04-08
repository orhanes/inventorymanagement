from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (View, CreateView, UpdateView)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Stock
from .forms import StockForm
from django_filters.views import FilterView
from .filters import StockFilter

# Stok/Ürün Listesi
class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(is_deleted=False)
    template_name = 'inventory.html'
    paginate_by = 10

#Stok/Ürün Ekleme
class StockCreateView(SuccessMessageMixin, CreateView):                                 # yeni stok eklemek için createview sınıfı, mesajı görüntülemek için kullanılan mixin
    model = Stock                                                                       # 'Stock' modelini model olarak ayarlama
    form_class = StockForm                                                              # 'StockForm' formunu form olarak ayarlama
    template_name = "edit_stock.html"                                                   # Şablon olarak 'edit_stock.html' kullanıldı
    success_url = '/inventory'                                                          # formu gönderdikten sonra URL'deki 'inventory' sayfasına yönlendiriyor
    success_message = "Ürün başarıyla eklendi."                                         # form gönderildiğinde mesajı görüntüler

    def get_context_data(self, **kwargs):                                               # ek içerik göndermek için kullanılır
        context = super().get_context_data(**kwargs)
        context["title"] = 'Yeni Ürün'
        context["savebtn"] = 'Ürün Ekle'
        return context       

# Stok/Ürün Güncelleme
class StockUpdateView(SuccessMessageMixin, UpdateView):                                 # Stokları düzenlemek için 'updateview' sınıfı, mesajı görüntülemek için kullanılan mixin
    model = Stock                                                                       # 'Stok' modelini model olarak ayarlama
    form_class = StockForm                                                              # 'StockForm' formunu form olarak ayarlama
    template_name = "edit_stock.html"                                                   # Şablon olarak 'edit_stock.html' kullanıldı
    success_url = '/inventory'                                                          # formu gönderdikten sonra URL'deki 'inventory' sayfasına yönlendiriyor
    success_message = "Ürün başarıyla güncellendi."                                     # form gönderildiğinde mesajı görüntüler

    def get_context_data(self, **kwargs):                                               # ek içerik göndermek için kullanılır
        context = super().get_context_data(**kwargs)
        context["title"] = 'Ürün Düzenle'
        context["savebtn"] = 'Güncelle'
        context["delbtn"] = 'Sil'
        return context

# Stok/Ürün Silme
class StockDeleteView(View):                                                            # ürünü silmek için view sınıfı
    template_name = "delete_stock.html"                                                 # Şablon olarak 'delete_stock.html' kullanıldı
    success_message = "Ürün başarıyla silindi."                                         # form gönderildiğinde mesajı görüntüler
    
    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object' : stock})

    def post(self, request, pk):  
        stock = get_object_or_404(Stock, pk=pk)
        stock.is_deleted = True
        stock.save()                                               
        messages.success(request, self.success_message)
        return redirect('inventory')