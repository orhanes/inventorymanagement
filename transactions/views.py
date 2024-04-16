from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (View, ListView, CreateView, UpdateView,DeleteView)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (PurchaseBill, Supplier, Buyer, PurchaseItem, PurchaseBillDetails, SaleBill, SaleItem, SaleBillDetails, Delivery, DeliveryBill, Receipt, ReceiptBill, MailOrder, MailOrderBill, Country, City, County, Department, Position)
from .forms import (SelectSupplierForm, PurchaseItemFormset, PurchaseDetailsForm, SupplierForm, BuyerForm, SelectBuyerForm, SaleItemFormset, SaleDetailsForm, DeliveryForm, ReceiptForm, MailOrderForm)
from inventory.models import Stock
from django_filters.views import FilterView
from .filters import BuyerFilter, SupplierFilter, DeliveryFilter, ReceiptFilter, MailOrderFilter

# Tedarikçi Listesi
class SupplierListView(FilterView):
    model = Supplier
    filterset_class = SupplierFilter
    template_name = "suppliers/suppliers_list.html"
    queryset = Supplier.objects.filter(is_deleted=False)
    paginate_by = 10

# Tedarikçi Ekle
class SupplierCreateView(SuccessMessageMixin, CreateView):
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
class SupplierUpdateView(SuccessMessageMixin, UpdateView):
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
class SupplierDeleteView(View):
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
class SupplierView(View):
    def get(self, request, name):
        supplierobj = get_object_or_404(Supplier, name=name)
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
class BuyerListView(FilterView):
    model = Buyer
    filterset_class = BuyerFilter
    template_name = "buyers/buyers_list.html"
    queryset = Buyer.objects.filter(is_deleted=False)
    paginate_by = 10

# Müşteri Ekle
class BuyerCreateView(SuccessMessageMixin, CreateView):
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
class BuyerUpdateView(SuccessMessageMixin, UpdateView):
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
class BuyerDeleteView(View):
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
class BuyerView(View):
    def get(self, request, name):
        buyerobj = get_object_or_404(Buyer, name=name)
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
class PurchaseView(ListView):
    model = PurchaseBill
    template_name = "purchases/purchases_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


# Tedarikçi Seçmek İçin
class SelectSupplierView(View):
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
class SelectBuyerView(View):
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


# Fatura nesnesi oluşturmak ve öğeleri kaydetmek için kullanılır
class PurchaseCreateView(View):                                                 
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
            for form in formset:                                               # for döngüsü her bir formu kendi nesnesi olarak kaydetmek için
                # false öğeyi kaydeder ve faturayı öğeye bağlar
                billitem = form.save(commit=False)
                billitem.billno = billobj                                       # fatura nesnesini ürünlere bağlar
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


# Satın Alma Faturasını Silme
class PurchaseDeleteView(SuccessMessageMixin, DeleteView):
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




# Satış Faturaları Listesi
class SaleView(ListView):
    model = SaleBill
    template_name = "sales/sales_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


# Satış Faturası Oluşturma ve Ürün Kaydetme
class SaleCreateView(View):                                                      
    template_name = 'sales/new_sale.html'

    def get(self, request, pk):
        formset = SaleItemFormset(request.GET or None)                      # boş bir formset oluşturur
        buyerobj = get_object_or_404(Buyer, pk=pk)                          # müşteri objesini alır
        context = {
            'formset'   : formset,
            'buyer'  : buyerobj,
        }                                                                   # müşteiyi ve formsetini context olarak gönderir
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = SaleItemFormset(request.POST)
        formset = SaleItemFormset(request.POST)    
        buyerobj = get_object_or_404(Buyer, pk=pk)          # formset için bir post yöntemi alır
          
        if form.is_valid() and formset.is_valid():
            # Faturayı kaydeder
            billobj = SaleBill(buyer=buyerobj)                        # Tedarikçi alanı 'supplierobj' olarak ayarlandığında 'SaleBill' sınıfının yeni bir nesnesi oluşturulur
            billobj.save()    
            # fatura ayrıntıları objesi oluşturur
            billdetailsobj = SaleBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:                                                # for döngüsü her bir formu kendi objesi olarak kaydetmesi için
                # false ürünü kaydeder ve faturayı ürüne bağlar
                billitem = form.save(commit=False)
                billitem.billno = billobj                                       # fatura nesnesini ürünlere bağlar
                # stok kalemini alır
                stock = get_object_or_404(Stock, name=billitem.stock.name)      
                # toplam fiyatı hesaplar
                billitem.totalprice = billitem.perprice * billitem.quantity
                # veritabanında stok miktarını günceller
                stock.quantity -= billitem.quantity   
                # fatura ürününü ve stoğu kaydeder
                stock.save()
                billitem.save()
            messages.success(request, "Satılan ürünler başarıyla kaydedildi.")
            return redirect('sale-bill', billno=billobj.billno)
       
        formset = SaleItemFormset(request.GET or None)
        context = {
            'formset'   : formset,
            'buyer'  : buyerobj,
        }
        return render(request, self.template_name, context)


# Satış Faturası Silme
class SaleDeleteView(SuccessMessageMixin, DeleteView):
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
class PurchaseBillView(View):
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


# Satış Faturası Görüntüleme
class SaleBillView(View):
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
            
            billdetailsobj.eway = request.POST.get("eway")    
            billdetailsobj.veh = request.POST.get("veh")
            billdetailsobj.destination = request.POST.get("destination")
            billdetailsobj.po = request.POST.get("po")
            billdetailsobj.cgst = request.POST.get("cgst")
            billdetailsobj.sgst = request.POST.get("sgst")
            billdetailsobj.igst = request.POST.get("igst")
            billdetailsobj.cess = request.POST.get("cess")
            billdetailsobj.tcs = request.POST.get("tcs")
            billdetailsobj.total = request.POST.get("total")

            billdetailsobj.save()
            messages.success(request, "Fatura bilgileri başarıyla değiştirildi.")
        
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)
    
# Nakliye Listesi
class DeliveryListView(FilterView):
    model = Delivery
    filterset_class = DeliveryFilter
    template_name = "deliveries/deliveries_list.html"
    queryset = Delivery.objects.filter(is_deleted=False)
    paginate_by = 10



# Nakliye Ekle
class DeliveryCreateView(SuccessMessageMixin, CreateView):
    model = Delivery
    form_class = DeliveryForm
    success_url = '/transactions/deliveries'
    success_message = "Nakliye başarıyla oluşturuldu."
    template_name = "deliveries/edit_delivery.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Yeni Nakliye'
        context["savebtn"] = 'Nakliye Ekle'
        return context     
  
# Nakliye Güncelle
class DeliveryUpdateView(SuccessMessageMixin, UpdateView):
    model = Delivery
    form_class = DeliveryForm
    success_url = '/transactions/deliveries'
    success_message = "Nakliye başarıyla güncellendi."
    template_name = "deliveries/edit_delivery.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Nakliye Güncelle'
        context["savebtn"] = 'Kaydet'
        context["delbtn"] = 'Sil'
        return context


# Nakliye Sil
class DeliveryDeleteView(View):
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
class DeliveryView(View):
    def get(self, request, id):
        deliveryobj = get_object_or_404(Delivery, id=id)
        # bill_list = PurchaseBill.objects.filter(delivery=deliveryobj)
        page = request.GET.get('page', 1)
        # paginator = Paginator(bill_list, 10)
        # try:
          #  bills = paginator.page(page)
        #except PageNotAnInteger:
         #   bills = paginator.page(1)
        #except EmptyPage:
         #   bills = paginator.page(paginator.num_pages)
        context = {
            'delivery'  : deliveryobj,
        #    'bills'     : bills
        }
        return render(request, 'deliveries/delivery.html', context)

# Malzeme Talep Fişi Görüntüleme
class DeliveryBillView(View):
    model = DeliveryBill
    template_name = "bill/delivery_bill.html"
    bill_base = "bill/bill_base.html"
    
    def get(self, request, billno):
        context = {
            'bill'          : Delivery.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)
    
# Tahsilat Makbuzu
class ReceiptListView(FilterView):
    model = Receipt
    filterset_class = ReceiptFilter
    template_name = "receipts/receipts_list.html"
    queryset = Receipt.objects.filter(is_deleted=False)
    paginate_by = 10

# Tahsilat Makbuzu Ekle
class ReceiptCreateView(SuccessMessageMixin, CreateView):
    model = Receipt
    form_class = ReceiptForm
    success_url = '/transactions/receipts'
    success_message = "Makbuz başarıyla oluşturuldu."
    template_name = "receipts/edit_receipt.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Yeni Tahsilat Makbuzu'
        context["savebtn"] = 'Makbuz Ekle'
        return context     
    
# Tahsilat Makbuzu Güncelle
class ReceiptUpdateView(SuccessMessageMixin, UpdateView):
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
        return context


# Tahsilat Makbuzu Sil
class ReceiptDeleteView(View):
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
class ReceiptView(View):
    def get(self, request, id):
        receiptobj = get_object_or_404(Receipt, id=id)
        # bill_list = PurchaseBill.objects.filter(receipt=receiptobj)
        page = request.GET.get('page', 1)
        # paginator = Paginator(bill_list, 10)
        # try:
         #   bills = paginator.page(page)
        # except PageNotAnInteger:
         #   bills = paginator.page(1)
        # except EmptyPage:
          #  bills = paginator.page(paginator.num_pages)
        context = {
            'receipt'  : receiptobj,
        #    'bills'     : bills
        }
        return render(request, 'receipts/receipt.html', context)

# Tahsilat Makbuzu Görüntüleme
class ReceiptBillView(View):
    model = ReceiptBill
    template_name = "bill/receipt_bill.html"
    bill_base = "bill/bill_base.html"
    
    def get(self, request, serial_number):
        context = {
            'bill'          : Receipt.objects.get(serial_number=serial_number),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

# Mail Order
class MailOrderListView(FilterView):
    model = MailOrder
    filterset_class = MailOrderFilter
    template_name = "mailorders/mailorders_list.html"
    queryset = MailOrder.objects.filter(is_deleted=False)
    paginate_by = 10

# Mail Order Ekle
class MailOrderCreateView(SuccessMessageMixin, CreateView):
    model = MailOrder
    form_class = MailOrderForm
    success_url = '/transactions/mailorders'
    success_message = "Mail Order başarıyla oluşturuldu."
    template_name = "mailorders/edit_mailorder.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Yeni Mail Order'
        context["savebtn"] = 'Mail Order Ekle'
        return context     
    
# Mail Order Güncelle
class MailOrderUpdateView(SuccessMessageMixin, UpdateView):
    model = MailOrder
    form_class = MailOrderForm
    success_url = '/transactions/mailorders'
    success_message = "Mail Order başarıyla güncellendi."
    template_name = "mailorders/edit_mailorder.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Mail Order Güncelle'
        context["savebtn"] = 'Kaydet'
        context["delbtn"] = 'Sil'
        return context


# Mail Order Sil
class MailOrderDeleteView(View):
    template_name = "mailorders/delete_mailorder.html"
    success_message = "Mail Order başarıyla silindi."

    def get(self, request, pk):
        mailorder = get_object_or_404(MailOrder, pk=pk)
        return render(request, self.template_name, {'object' : mailorder})

    def post(self, request, pk):  
        mailorder = get_object_or_404(MailOrder, pk=pk)
        mailorder.is_deleted = True
        mailorder.save()                                               
        messages.success(request, self.success_message)
        return redirect('mailorders-list')

# Mail Order Göster
class MailOrderView(View):
    def get(self, request, id):
        mailorderobj = get_object_or_404(MailOrder, id=id)
        # bill_list = PurchaseBill.objects.filter(receipt=receiptobj)
        page = request.GET.get('page', 1)
        # paginator = Paginator(bill_list, 10)
        # try:
         #   bills = paginator.page(page)
        # except PageNotAnInteger:
         #   bills = paginator.page(1)
        # except EmptyPage:
          #  bills = paginator.page(paginator.num_pages)
        context = {
            'mailorder'  : mailorderobj,
        #    'bills'     : bills
        }
        return render(request, 'mailorders/mailorder.html', context)

# Mail Order Makbuz Görüntüleme
class MailOrderBillView(View):
    model = MailOrderBill
    template_name = "bill/mailorder_bill.html"
    bill_base = "bill/bill_base.html"
    
    def get(self, request, id):
        context = {
            'bill'          : MailOrder.objects.get(id=id),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

# Ülkeye Göre Şehir Seçimi Müşteri
def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).all()
    return render(request, 'buyers/city_dropdown_list_options.html', {'cities': cities})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

# Şehre Göre İlçe Seçimi Müşteri
def load_counties(request):
    city_id = request.GET.get('city_id')
    counties = County.objects.filter(city_id=city_id).all()
    return render(request, 'buyers/county_dropdown_list_options.html', {'counties': counties})

# Departmana Göre Pozisyon Seçimi Müşteri
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

# Şehre Göre İlçe Seçimi Tedarikçi
def load_counties_supplier(request):
    city_id = request.GET.get('city_id')
    counties = County.objects.filter(city_id=city_id).all()
    return render(request, 'suppliers/county_dropdown_list_options.html', {'counties': counties})

# Departmana Göre Pozisyon Seçimi Tedarikçi
def load_positions_supplier(request):
    department_id = request.GET.get('department_id')
    positions = Position.objects.filter(department_id=department_id).all()
    return render(request, 'suppliers/position_dropdown_list_options.html', {'positions': positions})