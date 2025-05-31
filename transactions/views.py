from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (View, ListView, CreateView, UpdateView,DeleteView)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render
from common.models import ContractStatus, OfferStatus
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (PurchaseBill, Supplier, Buyer, PurchaseItem, PurchaseBillDetails, SaleBill, SaleItem, SaleBillDetails, Delivery, DeliveryBill, Receipt, ReceiptPayment, ReceiptBill, MailOrder, MailOrderBill, Country, City, County, Department, Position, Offer, OfferItem, Contract, ContractItem, ContractInstallment, PaymentMethod)
from .forms import (SelectSupplierForm, PurchaseItemFormset, PurchaseDetailsForm, SupplierForm, BuyerForm, SelectBuyerForm, SaleItemFormset, SaleDetailsForm, DeliveryForm, ReceiptForm, MailOrderForm, OfferForm, OfferItemFormSet, ContractForm, ContractItemFormSet, ContractInstallmentFormSet, ReceiptPaymentForm)
from inventory.models import Stock
from django_filters.views import FilterView
from .filters import BuyerFilter, SupplierFilter, DeliveryFilter, ReceiptFilter, MailOrderFilter
import json
from decimal import Decimal, InvalidOperation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import date
from django.db import models
from common.models import Company
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from django import forms

# Tedarikçi Listesi
class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = "suppliers/suppliers_list.html"
    context_object_name = 'object_list'
    paginate_by = 10  # Her sayfada 10 kayıt göster

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Tedarikçi adına göre filtreleme
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
            
        # Telefona göre filtreleme
        phone = self.request.GET.get('phone')
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
            
        # Email'e göre filtreleme
        email = self.request.GET.get('email')
        if email:
            queryset = queryset.filter(email__icontains=email)
            
        # Sıralama
        sort = self.request.GET.get('sort')
        if sort == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort == 'name_desc':
            queryset = queryset.order_by('-name')
        elif sort == 'phone_asc':
            queryset = queryset.order_by('phone')
        elif sort == 'phone_desc':
            queryset = queryset.order_by('-phone')
            
        return queryset

# Tedarikçi Ekle
class SupplierCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transactions/suppliers'
    success_message = "Tedarikçi başarıyla oluşturuldu."
    template_name = "suppliers/edit_supplier.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Yeni Tedarikçi'
        context["savebtn"] = 'Tedarikçi Ekle'
        return context     

# Tedarikçi Güncelle
class SupplierUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transactions/suppliers'
    success_message = "Tedarikçi başarıyla güncellendi."
    template_name = "suppliers/edit_supplier.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Tedarikçi Güncelle'
        context["savebtn"] = 'Kaydet'
        context["delbtn"] = 'Sil'
        return context


# Tedarikçi Sil
class SupplierDeleteView(LoginRequiredMixin, View):
    template_name = "suppliers/delete_supplier.html"
    success_message = "Tedarikçi başarıyla silindi."

    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return render(request, self.template_name, {'object' : supplier})

    def post(self, request, pk):  
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.is_deleted = True
        supplier.save()                                               
        messages.success(request, self.success_message)
        return redirect('suppliers-list')


# Tedarikçi Göster
class SupplierView(LoginRequiredMixin, View):
    def get(self, request, pk):
        supplierobj = get_object_or_404(Supplier, pk=pk)
        bill_list = PurchaseBill.objects.filter(supplier=supplierobj)
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 10)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'supplier'  : supplierobj,
            'bills'     : bills
        }
        return render(request, 'suppliers/supplier.html', context)

# Müşteri Listesi
class BuyerListView(LoginRequiredMixin, ListView):
    model = Buyer
    template_name = "buyers/buyers_list.html"
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Müşteri adına göre filtreleme
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
            
        # Telefona göre filtreleme
        phone = self.request.GET.get('phone')
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
            
        # Email'e göre filtreleme
        email = self.request.GET.get('email')
        if email:
            queryset = queryset.filter(email__icontains=email)
            
        # Sıralama
        sort = self.request.GET.get('sort')
        if sort == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort == 'name_desc':
            queryset = queryset.order_by('-name')
        elif sort == 'phone_asc':
            queryset = queryset.order_by('phone')
        elif sort == 'phone_desc':
            queryset = queryset.order_by('-phone')
            
        return queryset

# Müşteri Ekle
class BuyerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Buyer
    form_class = BuyerForm
    success_url = '/transactions/buyers'
    success_message = "Müşteri başarıyla oluşturuldu."
    template_name = "buyers/edit_buyer.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Yeni Müşteri'
        context["savebtn"] = 'Müşteri Ekle'
        return context  
    
# Müşteri Güncelle
class BuyerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Buyer
    form_class = BuyerForm
    success_url = '/transactions/buyers'
    success_message = "Müşteri başarıyla güncellendi."
    template_name = "buyers/edit_buyer.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Müşteri Güncelle'
        context["savebtn"] = 'Kaydet'
        context["delbtn"] = 'Sil'

        return context
    
    
# Müşteri Sil
class BuyerDeleteView(LoginRequiredMixin, View):
    template_name = "buyers/delete_buyer.html"
    success_message = "Müşteri başarıyla silindi."

    def get(self, request, pk):
        buyer = get_object_or_404(Buyer, pk=pk)
        return render(request, self.template_name, {'object' : buyer})

    def post(self, request, pk):  
        buyer = get_object_or_404(Buyer, pk=pk)
        buyer.is_deleted = True
        buyer.save()                                               
        messages.success(request, self.success_message)
        return redirect('buyers-list')


# Müşteri Göster
class BuyerView(LoginRequiredMixin, View):
    def get(self, request, pk):
        buyerobj = get_object_or_404(Buyer, pk=pk)
        bill_list = SaleBill.objects.filter(buyer=buyerobj)
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 10)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'buyer'  : buyerobj,
            'bills'  : bills
        }
        return render(request, 'buyers/buyer.html', context)


# Satınalm Fatura Bilgileri
class PurchaseView(LoginRequiredMixin, ListView):
    model = PurchaseBill
    template_name = "purchases/purchases_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Tedarikçi adına göre filtreleme
        supplier = self.request.GET.get('supplier')
        if supplier:
            queryset = queryset.filter(supplier__name__icontains=supplier)
            
        # Form numarasına göre filtreleme
        billno = self.request.GET.get('billno')
        if billno:
            queryset = queryset.filter(billno__icontains=billno)
            
        # Tarih aralığına göre filtreleme
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(time__date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(time__date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(time__date__lte=end_date)
            
        # Sıralama
        sort = self.request.GET.get('sort')
        if sort == 'date_asc':
            queryset = queryset.order_by('time')
        elif sort == 'date_desc':
            queryset = queryset.order_by('-time')
        elif sort == 'amount_asc':
            queryset = sorted(queryset, key=lambda x: x.get_total_amount())
        elif sort == 'amount_desc':
            queryset = sorted(queryset, key=lambda x: x.get_total_amount(), reverse=True)
            
        return queryset


# Tedarikçi Seçmek İçin
class SelectSupplierView(LoginRequiredMixin, View):
    form_class = SelectSupplierForm
    template_name = 'purchases/select_supplier.html'

    def get(self, request, *args, **kwargs):                                    # form sayfasını çağırır
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):                                   # seçilen tedarikçiyi alır ve 'PurchaseCreateView' sınıfına yönlendirir
        form = self.form_class(request.POST)
        if form.is_valid():
            supplierid = request.POST.get("supplier")
            supplier = get_object_or_404(Supplier, id=supplierid)
            return redirect('new-purchase', supplier.pk)
        return render(request, self.template_name, {'form': form})

 # Müşteri Seçmek İçin
class SelectBuyerView(LoginRequiredMixin, View):
    form_class = SelectBuyerForm
    template_name = 'sales/select_buyer.html'

    def get(self, request, *args, **kwargs):                                    # form sayfasını çağırır
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):                                   # seçilen tedarikçiyi alır ve 'PurchaseCreateView' sınıfına yönlendirir
        form = self.form_class(request.POST)
        if form.is_valid():
            buyerid = request.POST.get("buyer")
            buyer = get_object_or_404(Buyer, id=buyerid)
            return redirect('new-sale', buyer.pk)
        return render(request, self.template_name, {'form': form})


# Form nesnesi oluşturmak ve öğeleri kaydetmek için kullanılır
class PurchaseCreateView(LoginRequiredMixin, View):                                                 
    template_name = 'purchases/new_purchase.html'

    def get(self, request, pk):
        formset = PurchaseItemFormset(request.GET or None)                      # boş bir formset oluşturur
        supplierobj = get_object_or_404(Supplier, pk=pk)                        # tedarikçi objesini alır
        context = {
            'formset'   : formset,
            'supplier'  : supplierobj,
        }                                                                       # tedarikçiyi ve formsetini context olarak gönderir
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = PurchaseItemFormset(request.POST)                             # formset için bir post yöntemi alır
        supplierobj = get_object_or_404(Supplier, pk=pk)                        # tedarikçi nesnesini alır
        if formset.is_valid():
            # faturayı kaydeder
            billobj = PurchaseBill(supplier=supplierobj)                        # Tedarikçi alanı 'supplierobj' olarak ayarlandığında 'PurchaseBill' sınıfının yeni bir nesnesi oluşturulur
            billobj.save()                                                      # objeyi veritabanına kaydeder
            # fatura ayrıntıları objesi oluşturur
            billdetailsobj = PurchaseBillDetails(billno=billobj)
            billdetailsobj.save()
            
            # İlk formdan irsaliye ve vade bilgilerini al
            first_form = formset.forms[0]
            waybill_no = first_form.cleaned_data.get('waybill_no')
            waybill_date = first_form.cleaned_data.get('waybill_date')
            due_date = first_form.cleaned_data.get('due_date')
            
            for i, form in enumerate(formset):                                               
                # false öğeyi kaydeder ve faturayı öğeye bağlar
                billitem = form.save(commit=False)
                billitem.billno = billobj                                       # fatura nesnesini ürünlere bağlar
                
                # İlk form değilse, irsaliye ve vade bilgilerini ilk formdan al
                if i > 0:
                    billitem.waybill_no = waybill_no
                    billitem.waybill_date = waybill_date
                    billitem.due_date = due_date
                
                # stok kalemini alır
                stock = get_object_or_404(Stock, name=billitem.stock.name)       # ürünleri alır
                # toplam fiyatı hesaplar
                billitem.totalprice = billitem.perprice * billitem.quantity
                # veritabanındaki stok miktarını günceller
                stock.quantity += billitem.quantity                              # miktarı günceller
                # fatura ürünü ve stoğu kaydeder
                stock.save()
                billitem.save()
            messages.success(request, "Satın alınan ürünler başarıyla kaydedildi")
            return redirect('purchase-bill', billno=billobj.billno)
        formset = PurchaseItemFormset(request.GET or None)
        context = {
            'formset'   : formset,
            'supplier'  : supplierobj
        }
        return render(request, self.template_name, context)
    
class PurchaseUpdateView(LoginRequiredMixin, View):
    template_name = 'purchases/edit_purchase.html'

    def get(self, request, billno):
        bill = get_object_or_404(PurchaseBill, billno=billno)
        items = PurchaseItem.objects.filter(billno=bill)
        supplier = bill.supplier
        
        # İlk öğeden irsaliye ve vade bilgilerini al
        first_item = items.first()
        initial_data = []
        for item in items:
            initial_data.append({
                'stock': item.stock,
                'quantity': item.quantity,
                'perprice': item.perprice,
                'tax_rate': item.tax_rate,
                'waybill_no': first_item.waybill_no,
                'waybill_date': first_item.waybill_date.strftime('%Y-%m-%d') if first_item.waybill_date else None,
                'due_date': first_item.due_date.strftime('%Y-%m-%d') if first_item.due_date else None,
            })
        
        formset = PurchaseItemFormset(initial=initial_data)
        
        context = {
            'formset': formset,
            'supplier': supplier,
            'bill': bill,
            'first_item': first_item,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        bill = get_object_or_404(PurchaseBill, billno=billno)
        supplier = bill.supplier
        formset = PurchaseItemFormset(request.POST)
        
        if formset.is_valid():
            # Mevcut öğeleri sil
            PurchaseItem.objects.filter(billno=bill).delete()
            
            # İlk formdan irsaliye ve vade bilgilerini al
            first_form = formset.forms[0]
            waybill_no = first_form.cleaned_data.get('waybill_no')
            waybill_date = first_form.cleaned_data.get('waybill_date')
            due_date = first_form.cleaned_data.get('due_date')
            
            for i, form in enumerate(formset):
                if form.cleaned_data:
                    billitem = form.save(commit=False)
                    billitem.billno = bill
                    
                    # İlk form değilse, irsaliye ve vade bilgilerini ilk formdan al
                    if i > 0:
                        billitem.waybill_no = waybill_no
                        billitem.waybill_date = waybill_date
                        billitem.due_date = due_date
                    
                    stock = get_object_or_404(Stock, name=billitem.stock.name)
                    billitem.totalprice = billitem.perprice * billitem.quantity
                    
                    # Stok miktarını güncelle
                    stock.quantity -= billitem.quantity
                    stock.save()
                    billitem.save()
            
            messages.success(request, "Satın alma başarıyla güncellendi")
            return redirect('purchase-bill', billno=bill.billno)
        
        context = {
            'formset': formset,
            'supplier': supplier,
            'bill': bill,
        }
        return render(request, self.template_name, context)


# Satın Alma Formu Silme
class PurchaseDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PurchaseBill
    template_name = "purchases/delete_purchase.html"
    success_url = '/transactions/purchases'
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = PurchaseItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity -= item.quantity
                stock.save()
        messages.success(self.request, "Satın alma faturası başarıyla silindi.")
        return super(PurchaseDeleteView, self).delete(*args, **kwargs)




# Satış Formları Listesi
class SaleView(LoginRequiredMixin, ListView):
    model = SaleBill
    template_name = "sales/sales_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10  # Her sayfada 10 kayıt göster

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Müşteri adına göre filtreleme
        buyer = self.request.GET.get('buyer')
        if buyer:
            queryset = queryset.filter(buyer__name__icontains=buyer)
            
        # Form numarasına göre filtreleme
        billno = self.request.GET.get('billno')
        if billno:
            queryset = queryset.filter(billno__icontains=billno)
            
        # Tarih aralığına göre filtreleme
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(time__date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(time__date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(time__date__lte=end_date)
            
        # Sıralama
        sort = self.request.GET.get('sort')
        if sort == 'date_asc':
            queryset = queryset.order_by('time')
        elif sort == 'date_desc':
            queryset = queryset.order_by('-time')
        elif sort == 'amount_asc':
            queryset = sorted(queryset, key=lambda x: x.get_total_amount())
        elif sort == 'amount_desc':
            queryset = sorted(queryset, key=lambda x: x.get_total_amount(), reverse=True)
            
        return queryset


# Satış Formu Oluşturma ve Ürün Kaydetme
class SaleCreateView(LoginRequiredMixin, View):
    template_name = 'sales/new_sale.html'

    def get(self, request, pk):
        buyer = get_object_or_404(Buyer, pk=pk)
        stocks = Stock.objects.all()
        
        # Stok verilerini JSON formatına dönüştür
        stocks_json = json.dumps([{
            'pk': stock.pk,
            'quantity': stock.quantity
        } for stock in stocks])
        
        formset = SaleItemFormset()
        
        return render(request, self.template_name, {
            'buyer': buyer,
            'formset': formset,
            'stocks_json': stocks_json
        })

    def post(self, request, pk):
        buyer = get_object_or_404(Buyer, pk=pk)
        formset = SaleItemFormset(request.POST)
        
        if formset.is_valid():
            billobj = SaleBill(buyer=buyer)
            billobj.save()
            
            # Fatura ayrıntıları objesi oluşturur
            billdetailsobj = SaleBillDetails(billno=billobj)
            billdetailsobj.save()
            
            # İlk formdan irsaliye ve vade bilgilerini al
            first_form = formset.forms[0]
            waybill_no = first_form.cleaned_data.get('waybill_no')
            waybill_date = first_form.cleaned_data.get('waybill_date')
            due_date = first_form.cleaned_data.get('due_date')
            
            for i, form in enumerate(formset):
                if form.cleaned_data:
                    sale_item = form.save(commit=False)
                    sale_item.billno = billobj
                    
                    # İlk form değilse, irsaliye ve vade bilgilerini ilk formdan al
                    if i > 0:
                        sale_item.waybill_no = waybill_no
                        sale_item.waybill_date = waybill_date
                        sale_item.due_date = due_date
                    
                    # Toplam fiyatı hesapla
                    sale_item.totalprice = Decimal(str(float(sale_item.perprice) * float(sale_item.quantity)))
                    
                    # Stok kontrolü ve güncelleme
                    stock = get_object_or_404(Stock, name=sale_item.stock.name)
                    if stock.quantity >= sale_item.quantity:
                        stock.quantity -= sale_item.quantity
                        stock.save()
                        sale_item.save()
                    else:
                        messages.error(request, f"{stock.name} için yeterli stok yok!")
                        return redirect('new-sale', pk=pk)
            
            messages.success(request, "Satış başarıyla kaydedildi.")
            return redirect('sale-bill', billno=billobj.billno)
        
        # Form geçersizse
        stocks = Stock.objects.all()
        stocks_json = json.dumps([{
            'pk': stock.pk,
            'quantity': stock.quantity
        } for stock in stocks])
        
        return render(request, self.template_name, {
            'buyer': buyer,
            'formset': formset,
            'stocks_json': stocks_json
        })


# Satış Faturası Silme
class SaleDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SaleBill
    template_name = "sales/delete_sale.html"
    success_url = '/transactions/sales'
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = SaleItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity += item.quantity
                stock.save()
        messages.success(self.request, "Satış faturası başarıyla silindi.")
        return super(SaleDeleteView, self).delete(*args, **kwargs)




# Satınalma Faturası Görüntüleme
class PurchaseBillView(LoginRequiredMixin, View):
    model = PurchaseBill
    template_name = "bill/purchase_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill'          : PurchaseBill.objects.get(billno=billno),
            'items'         : PurchaseItem.objects.filter(billno=billno),
            'billdetails'   : PurchaseBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = PurchaseDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = PurchaseBillDetails.objects.get(billno=billno)
            
            billdetailsobj.po = request.POST.get("po")
            billdetailsobj.total = request.POST.get("total")

            billdetailsobj.save()
            messages.success(request, "Fatura bilgileri başarıyla değiştirildi")
        context = {
            'bill'          : PurchaseBill.objects.get(billno=billno),
            'items'         : PurchaseItem.objects.filter(billno=billno),
            'billdetails'   : PurchaseBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)


# Satış Formu Görüntüleme
class SaleBillView(LoginRequiredMixin, View):
    model = SaleBill
    template_name = "bill/sale_bill.html"
    bill_base = "bill/bill_base.html"
    
    def get(self, request, billno):
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = SaleDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = SaleBillDetails.objects.get(billno=billno)
            
            billdetailsobj.po = request.POST.get("po")
            billdetailsobj.total = request.POST.get("total")

            billdetailsobj.save()
            messages.success(request, "Form bilgileri başarıyla değiştirildi")
        
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)
    
# Nakliye Listesi
class DeliveryListView(LoginRequiredMixin, FilterView):
    model = Delivery
    filterset_class = DeliveryFilter
    template_name = "deliveries/deliveries_list.html"
    queryset = Delivery.objects.filter(is_deleted=False)
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request.GET
        # Form No
        delivery_number = request.get('delivery_number')
        if delivery_number:
            queryset = queryset.filter(delivery_number__icontains=delivery_number)
        # Firma/Kurum Adı
        buyer_name = request.get('buyer_name')
        if buyer_name:
            queryset = queryset.filter(buyer__name__icontains=buyer_name)
        # Nakliye Türü
        delivery_type = request.get('delivery_type')
        if delivery_type:
            queryset = queryset.filter(delivery_type__name__icontains=delivery_type)
        # Nakliye Firması
        delivery_company = request.get('delivery_company')
        if delivery_company:
            queryset = queryset.filter(delivery_company__name__icontains=delivery_company)
        # Tarih Aralığı
        start_date = request.get('start_date')
        end_date = request.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(sending_date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(sending_date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(sending_date__lte=end_date)
        # Sıralama
        sort = request.get('sort')
        if sort == 'date_asc':
            queryset = queryset.order_by('sending_date')
        elif sort == 'date_desc':
            queryset = queryset.order_by('-sending_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import DeliveryType, DeliveryCompany
        context['delivery_types'] = DeliveryType.objects.filter(is_active=True)
        context['delivery_companies'] = Delivery.objects.exclude(delivery_company=None).values_list('delivery_company__name', flat=True).distinct()
        # delivery_companies bir isim listesi, dropdown için model objesi listesine dönüştürelim
        context['delivery_companies'] = [{'name': name} for name in context['delivery_companies'] if name]
        return context

# Nakliye Ekle
class DeliveryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Delivery
    form_class = DeliveryForm
    success_url = '/transactions/deliveries'
    success_message = "Nakliye başarıyla oluşturuldu."
    template_name = "deliveries/edit_delivery.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Yeni Nakliye/Kargo'
        context["savebtn"] = 'Nakliye/Kargo Ekle'
        # Geçici numara üret
        from django.utils import timezone
        current_year = timezone.now().year
        last_delivery = Delivery.objects.filter(year=current_year).order_by('sequence').last()
        next_sequence = 1
        if last_delivery:
            next_sequence = last_delivery.sequence + 1
        preview_number = f"{current_year}/{str(next_sequence).zfill(4)}"
        context["preview_delivery_number"] = preview_number
        return context
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Kayıt sırasında bir hata oluştu: {str(e)}")
            return self.form_invalid(form)

# Nakliye Güncelle
class DeliveryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Delivery
    form_class = DeliveryForm
    success_url = '/transactions/deliveries'
    success_message = "Nakliye başarıyla güncellendi."
    template_name = "deliveries/edit_delivery.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Nakliye/Kargo Güncelle'
        context["savebtn"] = 'Kaydet'
        context["delbtn"] = 'Sil'
        if self.object and hasattr(self.object, 'delivery_number'):
            context["preview_delivery_number"] = self.object.delivery_number

        # Satış kalemi ve alıcı için initial değerleri ata
        if self.object.sale_item:
            context['form'].initial['sale_item_select'] = self.object.sale_item
            if getattr(self.object.sale_item, 'custom_name', None):
                context['form'].initial['sale_item_manual'] = self.object.sale_item.custom_name
        if self.object.buyer:
            context['form'].initial['buyer_select'] = self.object.buyer
            if getattr(self.object.buyer, 'name', None) and self.object.buyer.name != "Elle Girilen Müşteri":
                context['form'].initial['buyer_manual'] = self.object.buyer.name

        # Tarih alanları için initial
        for field in ['sending_date', 'estimated_delivery_date', 'actual_delivery_date']:
            value = getattr(self.object, field, None)
            if value:
                context['form'].initial[field] = value.strftime('%Y-%m-%d')

        # Araç/kargo/kurye alanları için initial
        for field in ['courier_name', 'courier_id', 'courier_number', 'courier_phone', 'vehicle_type', 'vehicle_plate']:
            value = getattr(self.object, field, None)
            if value:
                context['form'].initial[field] = value

        # Diğer alanlar için initial
        for field in ['delivery_type', 'billno', 'deliverer', 'status', 'waybill_number', 'description']:
            value = getattr(self.object, field, None)
            if value:
                context['form'].initial[field] = value

        # Alan gösterme mantığı
        delivery = self.get_object()
        if delivery.delivery_type:
            if delivery.delivery_type.name == 'ARAÇ':
                context['show_vehicle_fields'] = True
            elif delivery.delivery_type.name == 'KARGO':
                context['show_cargo_fields'] = True
            elif delivery.delivery_type.name == 'POSTA':
                context['show_mail_fields'] = True
            elif delivery.delivery_type.name == 'KURYE':
                context['show_courier_fields'] = True
        return context
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Güncelleme sırasında bir hata oluştu: {str(e)}")
            return self.form_invalid(form)
    
        

# Nakliye Sil
class DeliveryDeleteView(LoginRequiredMixin, View):
    template_name = "deliveries/delete_delivery.html"
    success_message = "Nakliye başarıyla silindi."

    def get(self, request, pk):
        delivery = get_object_or_404(Delivery, pk=pk)
        return render(request, self.template_name, {'object' : delivery})

    def post(self, request, pk):  
        delivery = get_object_or_404(Delivery, pk=pk)
        delivery.is_deleted = True
        delivery.save()                                               
        messages.success(request, self.success_message)
        return redirect('deliveries-list')

# Nakliye Göster
class DeliveryView(LoginRequiredMixin, View):
    def get(self, request, id):
        deliveryobj = get_object_or_404(Delivery, id=id)
        # bill_list = PurchaseBill.objects.filter(delivery=deliveryobj)
        page = request.GET.get('page', 1)
        # paginator = Paginator(bill_list, 10)
        # try:
          #  bills = paginator.page(page)
        # except PageNotAnInteger:
         #   bills = paginator.page(1)
        # except EmptyPage:
          #  bills = paginator.page(paginator.num_pages)
        context = {
            'delivery'  : deliveryobj,
        #    'bills'     : bills
        }
        return render(request, 'deliveries/delivery.html', context)

# Malzeme Talep Fişi Görüntüleme
class DeliveryBillView(LoginRequiredMixin, View):
    model = DeliveryBill
    template_name = "bill/delivery_bill.html"
    bill_base = "bill/bill_base.html"
    
    def get(self, request, billno):
        delivery = get_object_or_404(Delivery, delivery_number=billno)
        # DeliveryBill oluştur veya al
        bill, created = DeliveryBill.objects.get_or_create(delivery=delivery)
        context = {
            'bill': delivery,
            'bill_base': self.bill_base,
            'company': bill.company
        }
        return render(request, self.template_name, context)
    
# Tahsilat Makbuzu
class ReceiptListView(LoginRequiredMixin, ListView):
    model = Receipt
    template_name = "receipts/receipts_list.html"
    context_object_name = 'object_list'
    paginate_by = 10
    ordering = ['-number']  # Varsayılan sıralama: Makbuz numarasına göre azalan sıralama

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Müşteri adına göre filtreleme
        buyer = self.request.GET.get('buyer')
        if buyer:
            queryset = queryset.filter(buyer__name__icontains=buyer)
            
        # Makbuz numarasına göre filtreleme
        number = self.request.GET.get('number')
        if number:
            queryset = queryset.filter(number__icontains=number)
            
        # Tarih aralığına göre filtreleme
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(created_date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(created_date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(created_date__lte=end_date)
            
        # Ödeme şekline göre filtreleme
        payment_method = self.request.GET.get('payment_method')
        if payment_method:
            queryset = queryset.filter(payment_method_id=payment_method)
            
        # Sıralama
        sort = self.request.GET.get('sort')
        if sort == 'date_asc':
            queryset = queryset.order_by('created_date')
        elif sort == 'date_desc':
            queryset = queryset.order_by('-created_date')
        elif sort == 'amount_asc':
            queryset = queryset.order_by('payment_total')
        elif sort == 'amount_desc':
            queryset = queryset.order_by('-payment_total')
        elif sort == 'number_asc':
            queryset = queryset.order_by('number')
        elif sort == 'number_desc':
            queryset = queryset.order_by('-number')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_methods'] = PaymentMethod.objects.all()
        return context

# Tahsilat Makbuzu Ekle
class ReceiptCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Receipt
    form_class = ReceiptForm
    success_url = '/transactions/receipts'
    success_message = "Makbuz başarıyla oluşturuldu."
    template_name = "receipts/edit_receipt.html"
    
    def get_initial(self):
        # Mevcut yılı al
        current_year = timezone.now().year
        
        # Bu yıla ait son makbuzu bul
        last_receipt = Receipt.objects.filter(
            number__startswith=f'{current_year}/'
        ).order_by('-number').first()
        
        if last_receipt and last_receipt.number:
            # Son makbuz numarasından sonraki numarayı al
            last_number = int(last_receipt.number.split('/')[-1])
            new_number = f"{current_year}/{str(last_number + 1).zfill(4)}"
        else:
            # Bu yıl için ilk makbuz
            new_number = f"{current_year}/0001"
            
        return {'number': new_number}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Yeni Tahsilat Makbuzu'
        context["savebtn"] = 'Makbuz Ekle'
        context["payment_form"] = ReceiptPaymentForm()
        # Boş bir payments listesi ekle
        context["payments"] = json.dumps([])
        return context
    
    def form_valid(self, form):
        try:
            receipt = form.save()
            # ReceiptBill oluştur
            ReceiptBill.objects.create(receipt=receipt)
            
            payment_methods = self.request.POST.getlist('payments_payment_method[]')
            payment_dates = self.request.POST.getlist('payments_date[]')
            payment_amounts = self.request.POST.getlist('payments_amount[]')
            payment_currencies = self.request.POST.getlist('payments_currency[]')
            payment_descriptions = self.request.POST.getlist('payments_description[]')
            for i in range(len(payment_dates)):
                if payment_methods[i] and payment_dates[i] and payment_amounts[i]:
                    ReceiptPayment.objects.create(
                        receipt=receipt,
                        payment_method_id=payment_methods[i],
                        date=payment_dates[i],
                        amount=payment_amounts[i],
                        currency_id=payment_currencies[i] if payment_currencies[i] else 1,
                        description=payment_descriptions[i] if payment_descriptions and len(payment_descriptions) > i else ""
                    )
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Kayıt sırasında bir hata oluştu: {str(e)}")
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        import sys
        print("FORM HATALARI:", form.errors, form.non_field_errors(), file=sys.stderr)
        return super().form_invalid(form)
    
# Tahsilat Makbuzu Güncelle
class ReceiptUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Receipt
    form_class = ReceiptForm
    success_url = '/transactions/receipts'
    success_message = "Makbuz başarıyla güncellendi."
    template_name = "receipts/edit_receipt.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Makbuz Güncelle'
        context["savebtn"] = 'Kaydet'
        context["delbtn"] = 'Sil'
        context["payment_form"] = ReceiptPaymentForm()
        
        # Mevcut ödemeleri al ve JSON formatına dönüştür
        payments = self.object.payments.all().order_by('id')
        payments_data = []
        for payment in payments:
            payments_data.append({
                'id': payment.id,
                'payment_method': {
                    'id': payment.payment_method.id,
                    'name': str(payment.payment_method)
                },
                'date': payment.date.strftime('%Y-%m-%d'),
                'amount': float(payment.amount),
                'description': payment.description,
                'currency': {
                    'id': payment.currency.id,
                    'symbol': payment.currency.symbol
                }
            })
        context["payments"] = json.dumps(payments_data)
        
        # Ünvan seçimi için
        if self.object.buyer:
            context['form'].initial['buyer_select'] = self.object.buyer
            context['form'].initial['buyer_manual'] = self.object.buyer.name
        
        # Tarih için
        if self.object.created_date:
            context['form'].initial['created_date'] = self.object.created_date.strftime('%Y-%m-%d')
        
        return context
    
    def form_valid(self, form):
        try:
            receipt = form.save()
            receipt.payments.all().delete()
            payment_methods = self.request.POST.getlist('payments_payment_method[]')
            payment_dates = self.request.POST.getlist('payments_date[]')
            payment_amounts = self.request.POST.getlist('payments_amount[]')
            payment_currencies = self.request.POST.getlist('payments_currency[]')
            payment_descriptions = self.request.POST.getlist('payments_description[]')
            for i in range(len(payment_dates)):
                if payment_methods[i] and payment_dates[i] and payment_amounts[i]:
                    ReceiptPayment.objects.create(
                        receipt=receipt,
                        payment_method_id=payment_methods[i],
                        date=payment_dates[i],
                        amount=payment_amounts[i],
                        currency_id=payment_currencies[i] if payment_currencies[i] else 1,
                        description=payment_descriptions[i] if payment_descriptions and len(payment_descriptions) > i else ""
                    )
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Güncelleme sırasında bir hata oluştu: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        import sys
        print("FORM HATALARI:", form.errors, form.non_field_errors(), file=sys.stderr)
        return super().form_invalid(form)


# Tahsilat Makbuzu Sil
class ReceiptDeleteView(LoginRequiredMixin, View):
    template_name = "receipts/delete_receipt.html"
    success_message = "Makbuz başarıyla silindi."

    def get(self, request, pk):
        receipt = get_object_or_404(Receipt, pk=pk)
        return render(request, self.template_name, {'object' : receipt})

    def post(self, request, pk):  
        receipt = get_object_or_404(Receipt, pk=pk)
        receipt.is_deleted = True
        receipt.save()                                               
        messages.success(request, self.success_message)
        return redirect('receipts-list')
    
# Tahsilat Makbuzu Göster
class ReceiptView(LoginRequiredMixin, View):
    def get(self, request, id):
        receiptobj = get_object_or_404(Receipt, id=id)
        payments = receiptobj.payments.all().order_by('id')  # Ödemeleri ID'ye göre sırala
        
        context = {
            'receipt': receiptobj,
            'payments': payments,
        }
        return render(request, 'receipts/receipt.html', context)

# Tahsilat Makbuzu Görüntüleme
class ReceiptBillView(LoginRequiredMixin, View):
    def get(self, request, id):
        receipt = get_object_or_404(Receipt, id=id)
        # ReceiptBill yoksa oluştur
        bill, created = ReceiptBill.objects.get_or_create(receipt=receipt)
        context = {
            'receipt': receipt,
            'bill': bill,
            'bill_base': 'bill/bill_base.html',
        }
        return render(request, 'bill/receipt_bill.html', context)

# Mail Order Listesi
class MailOrderListView(LoginRequiredMixin, ListView):
    model = MailOrder
    template_name = 'mailorders/mailorders_list.html'
    context_object_name = 'mailorders'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Müşteri adına göre filtreleme
        customer_name = self.request.GET.get('customer_name')
        if customer_name:
            queryset = queryset.filter(customer_name__icontains=customer_name)
            
        # Telefona göre filtreleme
        phone = self.request.GET.get('phone')
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
            
        # Bankaya göre filtreleme
        bank = self.request.GET.get('bank')
        if bank:
            queryset = queryset.filter(bank__name__icontains=bank)
            
        # Tarih aralığına göre filtreleme
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(date__lte=end_date)
            
        # Sıralama
        sort = self.request.GET.get('sort')
        if sort == 'date_asc':
            queryset = queryset.order_by('date')
        elif sort == 'date_desc':
            queryset = queryset.order_by('-date')
        elif sort == 'amount_asc':
            queryset = queryset.order_by('amount')
        elif sort == 'amount_desc':
            queryset = queryset.order_by('-amount')
        else:
            # Varsayılan sıralama: Önce yıla göre, sonra numaraya göre azalan sıralama
            queryset = queryset.order_by('-number')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mail Order Listesi'
        context['customer_name'] = self.request.GET.get('customer_name', '')
        context['phone'] = self.request.GET.get('phone', '')
        context['bank'] = self.request.GET.get('bank', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        context['sort'] = self.request.GET.get('sort', '')
        return context

# Mail Order Ekle
class MailOrderCreateView(LoginRequiredMixin, CreateView):
    model = MailOrder
    form_class = MailOrderForm
    template_name = 'mailorders/edit_mailorder.html'
    success_url = reverse_lazy('mailorders-list')

    def get_initial(self):
        from datetime import datetime
        current_year = datetime.now().year
        last_order = MailOrder.objects.filter(number__startswith=f'{current_year}/').order_by('-id').first()
        next_id = (last_order.id + 1) if last_order else 1
        new_number = f"{current_year}/{str(next_id).zfill(4)}"
        while MailOrder.objects.filter(number=new_number).exists():
            next_id += 1
            new_number = f"{current_year}/{str(next_id).zfill(4)}"
        return {'number': new_number, 'user': self.request.user}

    def form_valid(self, form):
        try:
            # Decimal dönüşümü
            amount = form.cleaned_data.get('amount')
            if amount:
                # Virgülü noktaya çevir
                if isinstance(amount, str):
                    amount = amount.replace(',', '.')
                form.instance.amount = Decimal(str(amount))

            form.instance.user = self.request.user
            response = super().form_valid(form)
            # MailOrder kaydedildikten sonra bill oluştur
            from .models import MailOrderBill
            if not hasattr(self.object, 'bill'):
                MailOrderBill.objects.create(mailorder=self.object)
            messages.success(self.request, "Mail Order başarıyla oluşturuldu.")
            return response
        except Exception as e:
            messages.error(self.request, f"Kayıt sırasında bir hata oluştu: {str(e)}")
            return self.form_invalid(form)

class MailOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = MailOrder
    form_class = MailOrderForm
    template_name = 'mailorders/edit_mailorder.html'
    success_url = reverse_lazy('mailorders-list')

    def get_queryset(self):
        return MailOrder.objects.all()

    def form_valid(self, form):
        try:
            # Decimal dönüşümü
            amount = form.cleaned_data.get('amount')
            if amount:
                if isinstance(amount, str):
                    amount = amount.replace(',', '.')
                form.instance.amount = Decimal(str(amount))
            form.instance.user = self.request.user
            messages.success(self.request, "Mail Order başarıyla güncellendi.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Güncelleme sırasında bir hata oluştu: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Hatalı alanları kullanıcıya göster
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{form.fields[field].label or field}: {error}")
        return super().form_invalid(form)

class MailOrderDeleteView(LoginRequiredMixin, View):
    template_name = "mailorders/delete_mailorder.html"
    success_message = "Mail Order başarıyla silindi."

    def get(self, request, pk):
        mailorder = get_object_or_404(MailOrder, pk=pk)
        return render(request, self.template_name, {'object' : mailorder})

    def post(self, request, pk):  
        mailorder = get_object_or_404(MailOrder, pk=pk)
        mailorder.is_active = False
        mailorder.save()                                               
        messages.success(request, self.success_message)
        return redirect('mailorders-list')

class MailOrderView(LoginRequiredMixin, View):
    def get(self, request, id):
        mailorderobj = get_object_or_404(MailOrder, id=id)
        context = {
            'mailorder'  : mailorderobj,
        }
        return render(request, 'mailorders/mailorder.html', context)

class MailOrderBillView(LoginRequiredMixin, View):
    def get(self, request, id):
        mailorder = get_object_or_404(MailOrder, id=id)
        context = {
            'mailorder': mailorder,
            'bill': mailorder.bill,
            'bill_base': 'bill/bill_base.html',
        }
        return render(request, 'bill/mailorder_bill.html', context)

# Ülkeye Göre Şehir Seçimi Müşteri
def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).all()
    return render(request, 'buyers/city_dropdown_list_options.html', {'cities': cities})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

# Şehre Göre İlçe Seçimi Müşteri
def load_counties(request):
    city_id = request.GET.get('city_id')
    counties = County.objects.filter(city_id=city_id).all()
    return render(request, 'buyers/county_dropdown_list_options.html', {'counties': counties})

# Departmana Göre Pozisyon Seçimi Müşteri
def load_positions(request):
    department_id = request.GET.get('department_id')
    positions = Position.objects.filter(department_id=department_id).all()
    return render(request, 'buyers/position_dropdown_list_options.html', {'positions': positions})

# Ülkeye Göre Şehir Seçimi Tedarikçi
def load_cities_supplier(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).all()
    return render(request, 'suppliers/city_dropdown_list_options.html', {'cities': cities})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

# Şehre Göre İlçe Seçimi Tedarikçi
def load_counties_supplier(request):
    city_id = request.GET.get('city_id')
    counties = County.objects.filter(city_id=city_id).all()
    return render(request, 'suppliers/county_dropdown_list_options.html', {'counties': counties})

# Departmana Göre Pozisyon Seçimi Tedarikçi
def load_positions_supplier(request):
    department_id = request.GET.get('department_id')
    positions = Position.objects.filter(department_id=department_id).all()
    return render(request, 'suppliers/position_dropdown_list_options.html', {'positions': positions})

class SaleUpdateView(LoginRequiredMixin, View):
    template_name = 'sales/edit_sale.html'

    def get(self, request, billno):
        bill = get_object_or_404(SaleBill, billno=billno)
        items = SaleItem.objects.filter(billno=bill)
        buyer = bill.buyer
        
        # İlk öğeden irsaliye ve vade bilgilerini al
        first_item = items.first()
        initial_data = []
        for item in items:
            initial_data.append({
                'stock': item.stock,
                'quantity': item.quantity,
                'perprice': item.perprice,
                'tax_rate': item.tax_rate,
                'waybill_no': first_item.waybill_no,
                'waybill_date': first_item.waybill_date.strftime('%Y-%m-%d') if first_item.waybill_date else None,
                'due_date': first_item.due_date.strftime('%Y-%m-%d') if first_item.due_date else None,
            })
        
        formset = SaleItemFormset(initial=initial_data)
        
        context = {
            'formset': formset,
            'buyer': buyer,
            'bill': bill,
            'first_item': first_item,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        bill = get_object_or_404(SaleBill, billno=billno)
        buyer = bill.buyer
        formset = SaleItemFormset(request.POST)
        
        if formset.is_valid():
            # Mevcut öğeleri sil
            SaleItem.objects.filter(billno=bill).delete()
            
            # İlk formdan irsaliye ve vade bilgilerini al
            first_form = formset.forms[0]
            waybill_no = first_form.cleaned_data.get('waybill_no')
            waybill_date = first_form.cleaned_data.get('waybill_date')
            due_date = first_form.cleaned_data.get('due_date')
            
            for i, form in enumerate(formset):
                if form.cleaned_data:
                    saleitem = form.save(commit=False)
                    saleitem.billno = bill
                    
                    # İlk form değilse, irsaliye ve vade bilgilerini ilk formdan al
                    if i > 0:
                        saleitem.waybill_no = waybill_no
                        saleitem.waybill_date = waybill_date
                        saleitem.due_date = due_date
                    
                    stock = get_object_or_404(Stock, name=saleitem.stock.name)
                    saleitem.totalprice = saleitem.perprice * saleitem.quantity
                    
                    # Stok miktarını güncelle
                    stock.quantity -= saleitem.quantity
                    stock.save()
                    saleitem.save()
            
            messages.success(request, "Satış başarıyla güncellendi")
            return redirect('sale-bill', billno=bill.billno)
        
        context = {
            'formset': formset,
            'buyer': buyer,
            'bill': bill,
        }
        return render(request, self.template_name, context)

class OfferListView(LoginRequiredMixin, ListView):
    model = Offer
    template_name = "offers/offer_list.html"
    context_object_name = "offers"
    paginate_by = 20

    def get_queryset(self):
        queryset = Offer.objects.all()
        
        # Arama parametreleri
        number = self.request.GET.get('number')
        institution = self.request.GET.get('institution')
        company = self.request.GET.get('company')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        # Filtreleme
        if number:
            queryset = queryset.filter(number__icontains=number)
        if institution:
            queryset = queryset.filter(
                models.Q(institution__name__icontains=institution) |
                models.Q(company__name__icontains=institution)
            )
        if company:
            queryset = queryset.filter(company__name__icontains=company)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # Sıralama parametresi
        sort = self.request.GET.get('sort', '-date')
        
        # Sıralama seçenekleri
        if sort == 'date_asc':
            queryset = queryset.order_by('date')
        elif sort == 'date_desc':
            queryset = queryset.order_by('-date')
        elif sort == 'number_asc':
            queryset = queryset.order_by('number')
        elif sort == 'number_desc':
            queryset = queryset.order_by('-number')
        elif sort == 'start_date':
            queryset = queryset.order_by('start_date')
        elif sort == '-start_date':
            queryset = queryset.order_by('-start_date')
        elif sort == 'end_date':
            queryset = queryset.order_by('end_date')
        elif sort == '-end_date':
            queryset = queryset.order_by('-end_date')
        else:
            queryset = queryset.order_by('-date', '-number')
            
        return queryset
    
class OfferCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Offer
    form_class = OfferForm
    template_name = "offers/edit_offer.html"
    success_url = '/transactions/offers'
    success_message = "Teklif başarıyla oluşturuldu."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OfferItemFormSet(self.request.POST)
        else:
            context['formset'] = OfferItemFormSet()
        context["title"] = 'Yeni Teklif'
        context["savebtn"] = 'Teklif Ekle'
        # Açıklama metninde dinamik değişim
        description = ""
        company = None
        contract_type = None
        
        # Form verilerini kontrol et
        if 'form' in context:
            form = context['form']
            if hasattr(form, 'initial') and form.initial:
                description = form.initial.get('description', '')
                company = form.initial.get('company')
                contract_type = form.initial.get('contract_type')
        
        # POST verilerini kontrol et
        if self.request.POST:
            description = self.request.POST.get('description', '')
            company_id = self.request.POST.get('company')
            if company_id:
                company = Company.objects.filter(id=company_id).first()
            contract_type = self.request.POST.get('contract_type')
        
        # Şirket bilgisini al
        if not company:
            company = Company.objects.filter(is_active=True).first()
        
        # Placeholder'ları değiştir
        if company:
            description = description.replace("{{ firma_adi }}", company.name if hasattr(company, 'name') else '')
            if getattr(company, 'bank_name', None):
                description = description.replace("{{ banka_adi }}", company.bank_name)
            if getattr(company, 'branch_code', None):
                description = description.replace("{{ sube_adi }}", str(company.branch_code))
            if getattr(company, 'iban_no', None):
                description = description.replace("{{ iban_no }}", company.iban_no)
        
        if contract_type:
            description = description.replace("{{ sozlesme_turu }}", str(contract_type))
        
        context['description'] = description
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        # Kurum bilgisini ayarla
        buyer = form.cleaned_data.get('buyer_select')
        institution = form.cleaned_data.get('institution')
        if buyer:
            form.instance.institution = buyer.name
        else:
            form.instance.institution = institution
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class OfferUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Offer
    form_class = OfferForm
    template_name = "offers/edit_offer.html"
    success_url = '/transactions/offers'
    success_message = "Teklif başarıyla güncellendi."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OfferItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OfferItemFormSet(instance=self.object)
        context["title"] = 'Teklif Güncelle'
        context["savebtn"] = 'Kaydet'
        context["delbtn"] = 'Sil'
        # Açıklama metninde dinamik değişim
        description = self.object.description or ""
        company = self.object.company if self.object else None
        contract_type = self.object.contract_type if self.object else None
        if not company:
            company = Company.objects.filter(is_active=True).first()
        if company:
            description = description.replace("{{ firma_adi }}", company.name if hasattr(company, 'name') else '')
            if getattr(company, 'bank_name', None):
                description = description.replace("{{ banka_adi }}", company.bank_name)
            if getattr(company, 'branch_code', None):
                description = description.replace("{{ sube_adi }}", str(company.branch_code))
            if getattr(company, 'iban_no', None):
                description = description.replace("{{ iban_no }}", company.iban_no)
        if contract_type:
            description = description.replace("{{ sozlesme_turu }}", str(contract_type))
        context['description'] = description
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        # Kurum bilgisini ayarla
        buyer = form.cleaned_data.get('buyer_select')
        institution = form.cleaned_data.get('institution')
        if buyer:
            form.instance.institution = buyer.name
        else:
            form.instance.institution = institution
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class OfferDeleteView(LoginRequiredMixin, View):
    template_name = "offers/delete_offer.html"
    success_message = "Teklif başarıyla iptal edildi."

    def get(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        return render(request, self.template_name, {'object': offer})

    def post(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        cancelled_status = OfferStatus.objects.get(name="İptal Edildi")
        offer.status = cancelled_status
        offer.save()
        messages.success(request, self.success_message)
        return redirect('offers-list')


class OfferDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        offer = get_object_or_404(Offer, pk=id)
        context = {
            'offer': offer,
            'items': offer.items.all()
        }
        return render(request, 'offers/offer.html', context)
    
class OfferBillView(LoginRequiredMixin, View):
    template_name = "bill/offer_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, id):
        offer = get_object_or_404(Offer, pk=id)
        context = {
            'bill': offer,
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

def cancel_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    cancelled_status = OfferStatus.objects.get(name="İptal Edildi")
    offer.status = cancelled_status
    offer.save()
    messages.success(request, "Teklif başarıyla iptal edildi.")
    return redirect('offers-list')

class ContractListView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = "contracts/contract_list.html"
    context_object_name = "contracts"
    paginate_by = 10

    def get_queryset(self):
        queryset = Contract.objects.all()
        # Arama parametreleri
        number = self.request.GET.get('number')
        institution = self.request.GET.get('institution')
        company = self.request.GET.get('company')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        # Filtreleme
        if number:
            queryset = queryset.filter(number__icontains=number)
        if institution:
            queryset = queryset.filter(
                models.Q(institution__name__icontains=institution) |
                models.Q(company__name__icontains=institution)
            )
        if company:
            queryset = queryset.filter(company__name__icontains=company)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(date__lte=end_date)
        # Sıralama
        sort = self.request.GET.get('sort', '-date')
        if sort == 'date_asc':
            queryset = queryset.order_by('date')
        elif sort == 'date_desc':
            queryset = queryset.order_by('-date')
        elif sort == 'number_asc':
            queryset = queryset.order_by('number')
        elif sort == 'number_desc':
            queryset = queryset.order_by('-number')
        elif sort == 'start_date':
            queryset = queryset.order_by('start_date')
        elif sort == '-start_date':
            queryset = queryset.order_by('-start_date')
        elif sort == 'end_date':
            queryset = queryset.order_by('end_date')
        elif sort == '-end_date':
            queryset = queryset.order_by('-end_date')
        else:
            queryset = queryset.order_by('-date', '-number')
        return queryset

class ContractCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/edit_contract.html"
    success_url = '/transactions/contracts'
    success_message = "Sözleşme başarıyla oluşturuldu."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ContractItemFormSet(self.request.POST)
            context['installment_formset'] = ContractInstallmentFormSet(self.request.POST, prefix='installment_form')
        else:
            context['formset'] = ContractItemFormSet()
            context['installment_formset'] = ContractInstallmentFormSet(prefix='installment_form')
        context["title"] = 'Yeni Sözleşme'
        context["savebtn"] = 'Sözleşme Ekle'
        # Önerilen numara
        year = timezone.now().year
        last_contract = Contract.objects.filter(number__startswith=f"{year}/").order_by('-number').first()
        if last_contract and last_contract.number:
            last_number = int(last_contract.number.split('/')[-1])
            suggested_number = f"{year}/{str(last_number + 1).zfill(4)}"
        else:
            suggested_number = f"{year}/0001"
        context["suggested_number"] = suggested_number
        
        # Açıklama metninde dinamik değişim
        description = ""
        company = None
        contract_type = None
        
        # Form verilerini kontrol et
        if self.request.POST:
            description = self.request.POST.get('description', '')
            company_id = self.request.POST.get('company')
            if company_id:
                company = Company.objects.filter(id=company_id).first()
            contract_type = self.request.POST.get('contract_type')
        else:
            # Form ilk yüklendiğinde modeldeki varsayılan metni kullan
            description = self.model._meta.get_field('description').default
            if 'form' in context and context['form'].initial:
                company = context['form'].initial.get('company')
                contract_type = context['form'].initial.get('contract_type')
        
        # Şirket bilgisini al
        if not company:
            company = Company.objects.filter(is_active=True).first()
        
        # Placeholder'ları değiştir
        if company:
            description = description.replace("{{ firma_adi }}", company.name if hasattr(company, 'name') else '')
            if getattr(company, 'bank_name', None):
                description = description.replace("{{ banka_adi }}", company.bank_name)
            if getattr(company, 'branch_code', None):
                description = description.replace("{{ sube_adi }}", str(company.branch_code))
            if getattr(company, 'iban_no', None):
                description = description.replace("{{ iban_no }}", company.iban_no)
        
        if contract_type:
            description = description.replace("{{ sozlesme_turu }}", str(contract_type))
        
        context['description'] = description
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        installment_formset = context['installment_formset']

        if formset.is_valid() and installment_formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            installment_formset.instance = self.object
            installment_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ContractUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/edit_contract.html"
    success_url = '/transactions/contracts'
    success_message = "Sözleşme başarıyla güncellendi."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ContractItemFormSet(self.request.POST, instance=self.object)
            context['installment_formset'] = ContractInstallmentFormSet(self.request.POST, instance=self.object, prefix='installment_form')
        else:
            context['formset'] = ContractItemFormSet(instance=self.object)
            context['installment_formset'] = ContractInstallmentFormSet(instance=self.object, prefix='installment_form')
        context["title"] = 'Sözleşme Güncelle'
        context["savebtn"] = 'Kaydet'
        context["delbtn"] = 'Sil'
        # Açıklama metninde dinamik değişim
        description = self.object.description or ""
        company = self.object.company if self.object else None
        contract_type = self.object.contract_type if self.object else None
        if not company:
            company = Company.objects.filter(is_active=True).first()
        if company:
            description = description.replace("{{ firma_adi }}", company.name if hasattr(company, 'name') else '')
            if getattr(company, 'bank_name', None):
                description = description.replace("{{ banka_adi }}", company.bank_name)
            if getattr(company, 'branch_code', None):
                description = description.replace("{{ sube_adi }}", str(company.branch_code))
            if getattr(company, 'iban_no', None):
                description = description.replace("{{ iban_no }}", company.iban_no)
        if contract_type:
            description = description.replace("{{ sozlesme_turu }}", str(contract_type))
        context['description'] = description
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        installment_formset = context['installment_formset']
        if formset.is_valid() and installment_formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            installment_formset.instance = self.object
            installment_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ContractDeleteView(LoginRequiredMixin, View):
    template_name = "contracts/delete_contract.html"
    success_message = "Sözleşme başarıyla iptal edildi."

    def get(self, request, pk):
        contract = get_object_or_404(Contract, pk=pk)
        return render(request, self.template_name, {'object': contract})

    def post(self, request, pk):
        contract = get_object_or_404(Contract, pk=pk)
        cancelled_status = ContractStatus.objects.get(name="İptal Edildi")
        contract.status = cancelled_status
        contract.save()
        messages.success(request, self.success_message)
        return redirect('contract-list')

class ContractDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        contract = get_object_or_404(Contract, pk=id)
        items = contract.items.all()
        installments = contract.installments.all()
        # Kalan gün hesabı 10 günden az ise kırmızı yap
        days_left = None
        if contract.end_date:
            days_left = (contract.end_date - date.today()).days
        # Açıklama metninde dinamik değişim
        description = contract.description or ""
        company = contract.company or Company.objects.filter(is_active=True).first()
        if company:
            description = description.replace("{{ firma_adi }}", company.name if hasattr(company, 'name') else '')
            if getattr(company, 'bank_name', None):
                description = description.replace("{{ banka_adi }}", company.bank_name)
            if getattr(company, 'branch_code', None):
                description = description.replace("{{ sube_adi }}", str(company.branch_code))
            if getattr(company, 'iban_no', None):
                description = description.replace("{{ iban_no }}", company.iban_no)
        if contract.contract_type:
            description = description.replace("{{ sozlesme_turu }}", str(contract.contract_type))
        context = {
            'contract': contract,
            'items': items,
            'installments': installments,
            'days_left': days_left,
            'description': description,
        }
        return render(request, 'contracts/contract.html', context)

class ContractBillView(LoginRequiredMixin, View):
    template_name = "bill/contract_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, id):
        contract = get_object_or_404(Contract, pk=id)
        context = {
            'bill': contract,
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)

def cancel_contract(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    cancelled_status = ContractStatus.objects.get(name="İptal Edildi")
    contract.status = cancelled_status
    contract.save()
    messages.success(request, "Sözleşme başarıyla iptal edildi.")
    return redirect('contract-list')

# Müşteri bilgilerini getiren AJAX view
def get_buyer_info(request, pk):
    buyer = get_object_or_404(Buyer, pk=pk)
    data = {
        'name': buyer.name,
        'phone': buyer.phone,
        'address': buyer.address
    }
    return JsonResponse(data)