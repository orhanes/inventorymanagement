from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (View, CreateView, UpdateView, DetailView, ListView, DeleteView)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Stock, StockCard, StockLog
from .forms import StockForm, StockCardForm
from common.models import Category, SubCategory
from django_filters.views import FilterView
from .filters import StockFilter
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StockCardSerializer, StockSerializer
from rest_framework import viewsets, permissions
import json
import openpyxl
from django.http import JsonResponse

def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id).order_by('name')
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)

# Stok/Ürün Listesi
class StockListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = "inventory.html"
    context_object_name = 'object_list'
    paginate_by = 15  # Her sayfada 15 kayıt göster

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Ürün adına göre filtreleme
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
            
        # Kategoriye göre filtreleme
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__id=category)
            
        # Alt kategoriye göre filtreleme
        subcategory = self.request.GET.get('subcategory')
        if subcategory:
            queryset = queryset.filter(subcategory__id=subcategory)
            
        # Stok durumuna göre filtreleme
        stock_status = self.request.GET.get('stock_status')
        if stock_status == 'low':
            queryset = queryset.filter(quantity__lt=10)  # 10'dan az stok
        elif stock_status == 'out':
            queryset = queryset.filter(quantity=0)  # Stokta yok
            
        # Sıralama
        sort = self.request.GET.get('sort')
        if sort == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort == 'name_desc':
            queryset = queryset.order_by('-name')
        elif sort == 'quantity_asc':
            queryset = queryset.order_by('quantity')
        elif sort == 'quantity_desc':
            queryset = queryset.order_by('-quantity')
        else:
            queryset = queryset.order_by('name')  # Varsayılan sıralama
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Tüm kategorileri context'e ekle
        context['categories'] = Category.objects.filter(is_deleted=False).order_by('name')
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('export_excel'):
            codes_json = request.POST.get('bulk_codes')
            codes = []
            if codes_json:
                try:
                    codes = [item['code'] for item in json.loads(request.POST.get('bulk_codes'))]
                except Exception:
                    pass
            results = []
            for code in codes:
                card = StockCard.objects.filter(
                    models.Q(serial_number=code) | models.Q(lot=code) | models.Q(pk__iexact=code)
                ).first()
                if card:
                    results.append({'type': 'Stok Kartı', 'Ürün': card.stock.name, 'Seri No': card.serial_number, 'Adet': card.quantity, 'Kod': code})
                    continue
                stock = Stock.objects.filter(
                    models.Q(serial_number=code) | models.Q(name__iexact=code) | models.Q(pk__iexact=code)
                ).first()
                if stock:
                    results.append({'type': 'Ürün', 'Ürün': stock.name, 'Seri No': stock.serial_number, 'Adet': stock.quantity, 'Kod': code})
                else:
                    results.append({'type': 'Bulunamadı', 'Ürün': '', 'Seri No': '', 'Adet': '', 'Kod': code})
            # Excel oluştur
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = 'Toplu Sorgu Sonuçları'
            headers = ['Kod', 'Tip', 'Ürün', 'Seri No', 'Adet']
            ws.append(headers)
            for row in results:
                ws.append([row['Kod'], row['type'], row['Ürün'], row['Seri No'], row['Adet']])
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=toplu_sorgu_sonuclari.xlsx'
            wb.save(response)
            return response
        codes = request.POST.get('bulk_barcodes', '').splitlines()
        codes = [c.strip() for c in codes if c.strip()]
        results = []
        for code in codes:
            card = StockCard.objects.filter(
                models.Q(serial_number=code) | models.Q(lot=code) | models.Q(pk__iexact=code)
            ).first()
            if card:
                results.append({'type': 'stockcard', 'card': card, 'stock': card.stock, 'code': code})
                continue
            stock = Stock.objects.filter(
                models.Q(serial_number=code) | models.Q(name__iexact=code) | models.Q(pk__iexact=code)
            ).first()
            if stock:
                results.append({'type': 'stock', 'stock': stock, 'code': code})
            else:
                results.append({'type': 'notfound', 'code': code})
        context = self.get_context_data()
        context['bulk_results'] = results
        return self.render_to_response(context)

#Stok/Ürün Ekleme
class StockCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = "edit_stock.html"
    success_url = '/inventory'
    success_message = "Ürün başarıyla eklendi."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Yeni Ürün'
        context["savebtn"] = 'Ürün Ekle'
        return context

# Stok/Ürün Güncelleme
class StockUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Stock
    form_class = StockForm
    template_name = "edit_stock.html"
    success_url = '/inventory'
    success_message = "Ürün başarıyla güncellendi."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Ürün Düzenle'
        context["savebtn"] = 'Güncelle'
        context["delbtn"] = 'Sil'
        return context

# Stok/Ürün Silme
class StockDeleteView(LoginRequiredMixin, View):
    template_name = "delete_stock.html"
    success_message = "Ürün başarıyla silindi."
    
    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object' : stock})

    def post(self, request, pk):  
        stock = get_object_or_404(Stock, pk=pk)
        stock.is_deleted = True
        stock.save()                                               
        messages.success(request, self.success_message)
        return redirect('inventory')
    
# Stok/Ürün Detay Görüntüleme
class StockDetailView(LoginRequiredMixin, DetailView):
    model = Stock
    template_name = 'view_stock.html'
    context_object_name = 'stock'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Ürün Detayı'
        context["savebtn"] = 'Güncelle'
        context["delbtn"] = 'Sil'
        context['is_stok_yonetici'] = self.request.user.is_authenticated and self.request.user.groups.filter(name='stok_yonetici').exists()
        return context

def print_stockcard(request, pk):
    stockcard = get_object_or_404(StockCard, pk=pk)
    return render(request, 'stockcard/print_card.html', {'stockcard': stockcard})

def add_stockcard(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)
    if request.method == 'POST':
        form = StockCardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.stock = stock
            card.save()
            return redirect('view-stock', pk=stock_id)
    else:
        form = StockCardForm(initial={'stock': stock})
    return render(request, 'stockcard/add_card.html', {'form': form, 'stock': stock})

class StockCardUpdateView(LoginRequiredMixin, UpdateView):
    model = StockCard
    form_class = StockCardForm
    template_name = 'stockcard/edit_card.html'

    def get_success_url(self):
        return reverse_lazy('view-stock', kwargs={'pk': self.object.stock.pk})

class StockCardDeleteView(LoginRequiredMixin, DeleteView):
    model = StockCard
    template_name = 'stockcard/delete_card.html'

    def get_success_url(self):
        return reverse_lazy('view-stock', kwargs={'pk': self.object.stock.pk})

def barcode_search(request):
    code = request.GET.get('barcode', '').strip()
    if not code:
        messages.warning(request, 'Lütfen bir barkod veya QR kodu girin.')
        return redirect('inventory')

    # Önce stok kartında ara
    card = StockCard.objects.filter(
        models.Q(serial_number=code) | models.Q(lot=code) | models.Q(pk__iexact=code)
    ).first()
    if card:
        StockLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='read',
            stock=card.stock,
            stockcard=card,
            details=f'Barkod/QR arama ile stok kartı okundu: {code}'
        )
        return redirect('view-stock', pk=card.stock.pk)

    # Sonra üründe ara
    stock = Stock.objects.filter(
        models.Q(serial_number=code) | models.Q(name__iexact=code) | models.Q(pk__iexact=code)
    ).first()
    if stock:
        StockLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='read',
            stock=stock,
            details=f'Barkod/QR arama ile ürün okundu: {code}'
        )
        return redirect('view-stock', pk=stock.pk)

    messages.warning(request, 'Girilen barkod/QR kodu ile eşleşen kayıt bulunamadı.')
    return redirect('inventory')

class StockCardLookupAPI(APIView):
    def get(self, request):
        code = request.GET.get('code', '').strip()
        if not code:
            return Response({'detail': 'Kod parametresi gerekli.'}, status=status.HTTP_400_BAD_REQUEST)

        card = StockCard.objects.filter(
            models.Q(serial_number=code) | models.Q(lot=code) | models.Q(pk__iexact=code)
        ).first()
        if card:
            return Response({'type': 'stockcard', 'result': StockCardSerializer(card).data})

        stock = Stock.objects.filter(
            models.Q(serial_number=code) | models.Q(name__iexact=code) | models.Q(pk__iexact=code)
        ).first()
        if stock:
            return Response({'type': 'stock', 'result': StockSerializer(stock).data})

        return Response({'detail': 'Kayıt bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)

class IsStockManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='stok_yonetici').exists()

class StockCardViewSet(viewsets.ModelViewSet):
    queryset = StockCard.objects.all()
    serializer_class = StockCardSerializer
    permission_classes = [IsStockManagerOrReadOnly]

    def perform_create(self, serializer):
        instance = serializer.save()
        StockLog.objects.create(
            user=self.request.user,
            action='create',
            stock=instance.stock,
            stockcard=instance,
            details='API ile stok kartı eklendi.'
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        StockLog.objects.create(
            user=self.request.user,
            action='update',
            stock=instance.stock,
            stockcard=instance,
            details='API ile stok kartı güncellendi.'
        )

    def perform_destroy(self, instance):
        StockLog.objects.create(
            user=self.request.user,
            action='delete',
            stock=instance.stock,
            stockcard=instance,
            details='API ile stok kartı silindi.'
        )
        instance.delete()
