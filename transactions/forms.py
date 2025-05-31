from django import forms
from django.forms import formset_factory, BaseFormSet
from .models import (Supplier, Buyer, PurchaseBill, PurchaseItem, PurchaseBillDetails, SaleBill, SaleItem,SaleBillDetails, Delivery,
                    Receipt, MailOrder, Country, City, County, Department, Position, Bank, Offer, OfferItem, OfferBill, Contract, ContractItem, ContractInstallment, ReceiptBill,
                    ReceiptPayment, DeliveryType, VehicleType, DeliveryCompany)
from inventory.models import Stock
from common.models import Company, TaxRates, Currency, OfferStatus
from django.forms.widgets import DateInput
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When, Value, IntegerField
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation

# Tedarikçi Seçme
class SelectSupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_deleted=False)
        self.fields['supplier'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = PurchaseBill
        fields = ['supplier']

# Müşteri Seçme
class SelectBuyerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['buyer'].queryset = Buyer.objects.filter(is_deleted=False)
        self.fields['buyer'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = SaleBill
        fields = ['buyer']

# Tek Bir Stok Kalemi Formunu Oluşturmak İçin Kullanılan Form
class PurchaseItemForm(forms.ModelForm):
    def __init__(self, *args, is_first_item=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true', 'placeholder':'Birim Fiyat Giriniz'})
        self.fields['tax_rate'].widget.attrs.update({'class': 'textinput form-control'})

        # Sadece ilk form için irsaliye ve vade bilgilerini göster
        if not is_first_item:
            del self.fields['waybill_no']
            del self.fields['waybill_date']
            del self.fields['due_date']
        else:
            self.fields['waybill_no'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'İrsaliye Numarası Giriniz', 'style': 'text-transform: uppercase;'})
            self.fields['waybill_date'].widget = forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            )
            self.fields['due_date'].widget = forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            )

    class Meta:
        model = PurchaseItem
        fields = ['stock', 'quantity', 'perprice', 'tax_rate', 'waybill_no', 'waybill_date', 'due_date']

# Birden fazla 'PurchaseItemForm' oluşturmak için kullanılan form seti
class BasePurchaseItemFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i, form in enumerate(self.forms):
            form.is_first_item = (i == 0)

PurchaseItemFormset = formset_factory(
    PurchaseItemForm,
    formset=BasePurchaseItemFormSet,
    extra=1
)

# satın alma faturasının diğer ayrıntılarını kabul etmek için kullanılan form
class PurchaseDetailsForm(forms.ModelForm):
    class Meta:
        model = PurchaseBillDetails
        fields = ['po', 'total']

# Tedarikçi Formu
class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Tedarikçi Firma/Kişi Adı Giriniz'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Tedarikçi Telefonu Giriniz'})
        self.fields['country'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['city'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['county'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['web'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Web Adresi Giriniz'})
        self.fields['representative'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Temsilci Ad/Soyad Giriniz'})
        self.fields['department'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['position'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['mobile_phone'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Cep Telefonu Giriniz'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Email Adresi Giriniz'})
        self.fields['tax_id'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Vergi Kimlik Numarası Giriniz' })
        self.fields['tax_administration'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Vergi Dairesi Giriniz'})
        self.fields['kep_address'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'KEP Adresi Giriniz'})
        self.fields['bank_name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['iban_no'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'IBAN Numarası Giriniz'})
        self.fields['branch_code'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Şube Kodu Giriniz'})
        self.fields['account_number'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Hesap Numarası Giriniz'})
        # self.fields['created_date'].widget.attrs.update({'class': 'textinput form-control'})

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['city'].queryset = City.objects.none()
            self.fields['county'].queryset = County.objects.none()
            self.fields['position'].queryset = Position.objects.none()
            
            if 'country' in self.data:
                try:
                    country_id = int(self.data.get('country'))
                    self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
            
            if 'city' in self.data:
                try:
                    city_id = int(self.data.get('city'))
                    self.fields['county'].queryset = County.objects.filter(city_id=city_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['county'].queryset = self.instance.city.county_set.order_by('name')

            
            if 'department' in self.data:
                try:
                    department_id = int(self.data.get('department'))
                    self.fields['position'].queryset = Position.objects.filter(department_id=department_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['position'].queryset = self.instance.department.position_set.order_by('name')


    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'address', 'country', 'city', 'county', 'web', 'representative', 'department', 'position', 
                  'mobile_phone', 'email', 'tax_id', 'tax_administration', 'kep_address', 'bank_name', 'iban_no', 'branch_code', 'account_number']
        widgets = {
            'address' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4',
                    'placeholder':' Tedarikçi Adresi Giriniz'
                }
            )
        }
        
# Müşteri Formu
class BuyerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Müşteri Adı Giriniz'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Müşteri Telefonu Giriniz'})
        self.fields['country'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['city'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['county'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['web'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Web Adresi Giriniz'})
        self.fields['representative'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Temsilci Adı Giriniz'})
        self.fields['department'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['position'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['mobile_phone'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Cep Telefonu Giriniz'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Email Giriniz'})
        self.fields['tax_id'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Vergi Kimlik No Giriniz'})
        self.fields['tax_administration'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Vergi Dairesi Giriniz'})
        self.fields['kep_address'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'KEP Adresi Giriniz'})
        self.fields['bank_name'].widget.attrs.update({'class': 'textinput form-control', 'title': 'İstenilen Biçimde Giriniz'})
        self.fields['iban_no'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'IBAN Numarası Giriniz'})
        self.fields['branch_code'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Şube Kodu Giriniz'})
        self.fields['account_number'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Hesap Numarası Giriniz'})

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['city'].queryset = City.objects.none()
            self.fields['county'].queryset = County.objects.none()
            self.fields['position'].queryset = Position.objects.none()
            
            if 'country' in self.data:
                try:
                    country_id = int(self.data.get('country'))
                    self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
            
            if 'city' in self.data:
                try:
                    city_id = int(self.data.get('city'))
                    self.fields['county'].queryset = County.objects.filter(city_id=city_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['county'].queryset = self.instance.city.county_set.order_by('name')

            
            if 'department' in self.data:
                try:
                    department_id = int(self.data.get('department'))
                    self.fields['position'].queryset = Position.objects.filter(department_id=department_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['position'].queryset = self.instance.department.position_set.order_by('name')


    class Meta:
        model = Buyer
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(
                attrs={
                    'class': 'textinput form-control',
                    'rows': '4',
                    'placeholder': 'Adres Giriniz'
                }
            ),
        }

#Tek bir stok kalemi formu oluşturmak için kullanılan form
class SaleItemForm(forms.ModelForm):
    def __init__(self, *args, is_first_item=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true', 'placeholder':'Birim Fiyat Giriniz'})
        self.fields['tax_rate'].widget.attrs.update({'class': 'textinput form-control'})

        # Sadece ilk form için irsaliye ve vade bilgilerini göster
        if not is_first_item:
            del self.fields['waybill_no']
            del self.fields['waybill_date']
            del self.fields['due_date']
        else:
            self.fields['waybill_no'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'İrsaliye Numarası Giriniz', 'style': 'text-transform: uppercase;'})
            self.fields['waybill_date'].widget = forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            )
            self.fields['due_date'].widget = forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            )

    class Meta:
        model = SaleItem
        fields = ['stock', 'quantity', 'perprice', 'tax_rate', 'waybill_no', 'waybill_date', 'due_date']

# Birden fazla 'SaleItemForm' oluşturmak için kullanılan form seti
class BaseSaleItemFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i, form in enumerate(self.forms):
            form.is_first_item = (i == 0)

SaleItemFormset = formset_factory(
    SaleItemForm,
    formset=BaseSaleItemFormSet,
    extra=1
)

# Satış faturasının diğer ayrıntılarını kabul etmek için kullanılan form
class SaleDetailsForm(forms.ModelForm):
    class Meta:
        model = SaleBillDetails
        fields = ['po', 'total']

# Nakliye Formu
class DeliveryForm(forms.ModelForm):
    sale_item_select = forms.ModelChoiceField(
        queryset=SaleItem.objects.all(),
        required=False,
        label='Mevcut Satıştan Seç',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sale_item_manual = forms.CharField(
        required=False,
        label='Satış Kalemi (Elle Gir)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Satış kalemi bilgilerini giriniz'})
    )
    buyer_select = forms.ModelChoiceField(
        queryset=Buyer.objects.all(),
        required=False,
        label='Mevcut Müşteriden Seç',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    buyer_manual = forms.CharField(
        required=False,
        label='Alıcı (Elle Gir)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alıcı bilgilerini giriniz'})
    )

    # ForeignKey alanlar
    vehicle_type = forms.ModelChoiceField(
        queryset=VehicleType.objects.filter(is_active=True),
        required=False,
        label='Araç Türü',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    delivery_company = forms.ModelChoiceField(
        queryset=DeliveryCompany.objects.filter(is_active=True),
        required=False,
        label='Nakliye Firması',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Diğer alanlar (modeldekiyle aynı isim ve tipte)
    tracking_number = forms.CharField(
        required=False,
        label='Takip Numarası',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Takip Numarası Giriniz'})
    )
    courier_name = forms.CharField(
        required=False,
        label='Şoför/Kurye Adı',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Şoför/Kurye Adı Giriniz'})
    )
    courier_id = forms.CharField(
        required=False,
        label='T.C. Kimlik No',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'T.C. Kimlik No Giriniz'})
    )
    courier_number = forms.CharField(
        required=False,
        label='Şoför/Kurye Numarası',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Şoför/Kurye Numarası Giriniz'})
    )
    courier_phone = forms.CharField(
        required=False,
        label='Telefon',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Telefon Giriniz'})
    )
    vehicle_plate = forms.CharField(
        required=False,
        label='Araç Plakası',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Araç Plakası Giriniz'})
    )
    explanation = forms.CharField(
        required=False,
        label='İzahat',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'İzahat Giriniz'})
    )
    address = forms.CharField(
        required=False,
        label='Adres',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adres Giriniz'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_type'].queryset = DeliveryType.objects.filter(is_active=True)
        self.fields['delivery_type'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['billno'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Fiş Numarası Giriniz'})
        self.fields['explanation'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'İzahat Giriniz'})
        self.fields['deliverer'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Teslim Eden Giriniz'})
        self.fields['tracking_number'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Takip Numarası Giriniz'})
        self.fields['courier_name'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Şoför/Kurye Adı Giriniz'})
        self.fields['courier_id'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'T.C. Kimlik No Giriniz', 'maxlength': '11', 'pattern' : '[0-9]+', 'title' : 'Sadece numerik karakterler'})
        self.fields['courier_phone'].widget.attrs.update({'class': 'textinput form-control', 'autocomplete': 'off', 'placeholder':'Telefon Giriniz', 'pattern':'[0-9]+', 'maxlength': '11', 'title' : 'Sadece numerik karakterler'})
        self.fields['courier_number'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Şoför/Kurye Numarası Giriniz'})
        self.fields['vehicle_plate'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Araç Plakası Giriniz'})
        self.fields['vehicle_type'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['delivery_company'].widget.attrs.update({'class': 'textinput form-control'})

    def clean(self):
        cleaned_data = super().clean()
        sale_item_choice = self.data.get('sale_item_choice')
        if sale_item_choice == 'select':
            sale_item = cleaned_data.get('sale_item_select')
            if not sale_item:
                self.add_error('sale_item_select', 'Lütfen bir satış kalemi seçiniz.')
            else:
                cleaned_data['final_sale_item'] = sale_item
                cleaned_data['final_buyer'] = sale_item.billno.buyer if sale_item.billno else None
        else:
            sale_item_manual = cleaned_data.get('sale_item_manual')
            if not sale_item_manual:
                self.add_error('sale_item_manual', 'Lütfen satış kalemi giriniz.')
            else:
                buyer = cleaned_data.get('buyer_select')
                if not buyer:
                    buyer_manual = cleaned_data.get('buyer_manual')
                    if buyer_manual:
                        from .models import Buyer
                        buyer, _ = Buyer.objects.get_or_create(name=buyer_manual)
                    else:
                        from .models import Buyer
                        buyer, _ = Buyer.objects.get_or_create(name="Elle Girilen Müşteri")
                from .models import SaleItem, SaleBill, Stock
                sale_bill = SaleBill.objects.create(buyer=buyer)
                stock = Stock.objects.first()
                sale_item = SaleItem.objects.create(
                    custom_name=sale_item_manual,
                    billno=sale_bill,
                    stock=stock
                )
                cleaned_data['final_sale_item'] = sale_item
                cleaned_data['final_buyer'] = buyer
        # Diğer alanların validasyonunu koru
        delivery_type = cleaned_data.get('delivery_type')
        if delivery_type:
            if delivery_type.name == 'ARAÇ':
                for field in ['vehicle_type', 'vehicle_plate', 'courier_name', 'courier_id', 'courier_phone', 'courier_number']:
                    if not cleaned_data.get(field):
                        self.add_error(field, f'{self.fields[field].label} girilmelidir.')
            elif delivery_type.name == 'KARGO':
                for field in ['delivery_company', 'tracking_number']:
                    if not cleaned_data.get(field):
                        self.add_error(field, f'{self.fields[field].label} girilmelidir.')
            elif delivery_type.name == 'POSTA':
                for field in ['delivery_company', 'tracking_number']:
                    if not cleaned_data.get(field):
                        self.add_error(field, f'{self.fields[field].label} girilmelidir.')
            elif delivery_type.name == 'KURYE':
                for field in ['courier_name', 'courier_id', 'courier_phone', 'courier_number']:
                    if not cleaned_data.get(field):
                        self.add_error(field, f'{self.fields[field].label} girilmelidir.')
        # Adres mantığı
        buyer = cleaned_data.get('final_buyer')
        address = cleaned_data.get('address')
        if buyer and hasattr(buyer, 'address') and buyer.address:
            cleaned_data['final_address'] = buyer.address
        elif address:
            cleaned_data['final_address'] = address
        else:
            cleaned_data['final_address'] = ''
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.sale_item = self.cleaned_data.get('final_sale_item')
        instance.buyer = self.cleaned_data.get('final_buyer')
        instance.address = self.cleaned_data.get('final_address')
        delivery_type = self.cleaned_data.get('delivery_type')
        if delivery_type:
            if delivery_type.name == 'ARAÇ':
                instance.vehicle_type = self.cleaned_data.get('vehicle_type')
                instance.vehicle_plate = self.cleaned_data.get('vehicle_plate')
                instance.courier_name = self.cleaned_data.get('courier_name')
                instance.courier_id = self.cleaned_data.get('courier_id')
                instance.courier_number = self.cleaned_data.get('courier_number')
                instance.courier_phone = self.cleaned_data.get('courier_phone')
                instance.explanation = self.cleaned_data.get('explanation')
                instance.tracking_number = None
                instance.delivery_company = None
            elif delivery_type.name == 'KARGO':
                instance.tracking_number = self.cleaned_data.get('tracking_number')
                instance.delivery_company = self.cleaned_data.get('delivery_company')
                instance.vehicle_type = None
                instance.vehicle_plate = None
                instance.courier_name = None
                instance.courier_id = None
                instance.courier_number = None
                instance.courier_phone = None
                instance.explanation = None
            elif delivery_type.name == 'POSTA':
                instance.tracking_number = self.cleaned_data.get('tracking_number')
                instance.delivery_company = self.cleaned_data.get('delivery_company')
                instance.vehicle_type = None
                instance.vehicle_plate = None
                instance.courier_name = None
                instance.courier_id = None
                instance.courier_number = None
                instance.courier_phone = None
                instance.explanation = None
            elif delivery_type.name == 'KURYE':
                instance.courier_name = self.cleaned_data.get('courier_name')
                instance.courier_id = self.cleaned_data.get('courier_id')
                instance.courier_number = self.cleaned_data.get('courier_number')
                instance.courier_phone = self.cleaned_data.get('courier_phone')
                instance.vehicle_type = self.cleaned_data.get('vehicle_type')
                instance.vehicle_plate = self.cleaned_data.get('vehicle_plate')
                instance.tracking_number = None
                instance.delivery_company = None
        if commit:
            instance.save()
        return instance
        
    class Meta:
        model = Delivery
        fields = [
            'delivery_type', 'vehicle_type', 'billno', 'explanation',
            'tracking_number', 'delivery_company', 'courier_name', 'courier_id', 
            'courier_phone', 'courier_number', 'vehicle_plate', 'description', 'tonage', 'analysed',
            'status', 'estimated_delivery_date', 'actual_delivery_date', 'waybill_number', 'deliverer', 'sending_date', 'address'
        ]
        widgets = {
            'description' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4',
                    'placeholder':'Nakliye ile ilgili notları giriniz'
                }
            ),
           'tonage' : forms.CheckboxInput(
                attrs = {
                  'style':'width:20px;height:20px'
                }
            ),
            'analysed' : forms.CheckboxInput(
                attrs = {
                  'style':'width:20px;height:20px'
                }
            ),
            'status' : forms.Select(
                attrs = {
                    'class' : 'textinput form-control'
                }
            ),
            'sending_date' : forms.DateInput(
                attrs = {
                    'class' : 'form-control',
                    'type' : 'date'
                }
            ),
            'estimated_delivery_date' : forms.DateInput(
                attrs = {
                    'class' : 'form-control',
                    'type' : 'date'
                }
            ),
            'actual_delivery_date' : forms.DateInput(
                attrs = {
                    'class' : 'form-control',
                    'type' : 'date'
                }
            ),
            'waybill_number' : forms.TextInput(
                attrs = {
                    'class' : 'textinput form-control',
                    'placeholder' : 'İrsaliye Numarası Giriniz'
                }
            )
        }
       
class ReceiptForm(forms.ModelForm):
    buyer_select = forms.ModelChoiceField(
        queryset=Buyer.objects.all(),
        required=False,
        label='Müşteri Seçin',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    buyer_manual = forms.CharField(
        required=False,
        label='Ünvan (Elle Gir)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Müşteri Adı Giriniz'})
    )
    payment_total = forms.DecimalField(
        required=False,
        label='Ödeme Toplamı (Rakam ile)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    payment_handwrite = forms.CharField(
        required=False,
        label='Ödeme Toplamı (Yazı ile)',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['buyer'].queryset = Buyer.objects.filter()
        self.fields['buyer'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['buyer'].required = False  # buyer alanını opsiyonel yap
        
        # Tarih alanı için
        if self.instance and self.instance.created_date:
            self.fields['created_date'].initial = self.instance.created_date
        
        self.fields['created_date'].widget.attrs.update({'class': 'dateinput form-control'})
        self.fields['payment_method'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['collector'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Tahsil Eden Adı/Soyadı Giriniz'})
        self.fields['number'].widget.attrs.update({'class': 'textinput form-control', 'readonly': 'readonly'})
      
    def clean(self):
        cleaned_data = super().clean()
        buyer_select = cleaned_data.get('buyer_select')
        buyer_manual = cleaned_data.get('buyer_manual')
        if not buyer_select and not buyer_manual:
            raise forms.ValidationError("Lütfen müşteri seçin veya elle girin.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        buyer_select = self.cleaned_data.get('buyer_select')
        buyer_manual = self.cleaned_data.get('buyer_manual')
        payment_total = self.cleaned_data.get('payment_total')
        payment_handwrite = self.cleaned_data.get('payment_handwrite')

        if buyer_select:
            instance.buyer = buyer_select
        elif buyer_manual:
            buyer_qs = Buyer.objects.filter(name=buyer_manual)
            if buyer_qs.exists():
                buyer = buyer_qs.first()
            else:
                buyer = Buyer.objects.create(name=buyer_manual)
            instance.buyer = buyer

        # DecimalField için güvenli atama
        try:
            instance.payment_total = Decimal(str(payment_total).replace(',', '.')) if payment_total not in [None, ''] else Decimal('0')
        except (InvalidOperation, ValueError):
            instance.payment_total = Decimal('0')

        instance.payment_handwrite = payment_handwrite

        if commit:
            instance.save()
        return instance

    class Meta:
        model = Receipt
        fields = ['buyer', 'buyer_select', 'buyer_manual', 'created_date', 'payment_method', 'collector', 'number', 'payment_total', 'payment_handwrite']

class ReceiptPaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Tutar Giriniz'})
        self.fields['date'].widget.attrs.update({'class': 'dateinput form-control'})
        self.fields['description'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Açıklama Giriniz'})
        self.fields['currency'].widget.attrs.update({'class': 'textinput form-control'})
        
    class Meta:
        model = ReceiptPayment
        fields = ['payment_method', 'amount', 'date', 'description', 'currency']

class MailOrderForm(forms.ModelForm):
    buyer_select = forms.ModelChoiceField(
        queryset=Buyer.objects.filter(is_deleted=False),
        required=False,
        label='Mevcut Müşteriden Seç',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = MailOrder
        fields = [
            'number', 'date', 'buyer_select', 'customer_name', 'phone', 'address',
            'bank', 'owner', 'card_number', 'security_code', 'expiry_month',
            'expiry_year', 'amount', 'amount_write', 'currency'
        ]
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kişi Adı/Soyadı veya Firma/Kurum Adı Giriniz'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon Numarası Giriniz'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Adres Giriniz'}),
            'bank': forms.Select(attrs={'class': 'form-control'}),
            'owner': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kart Sahibi Adı Giriniz'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kart Numarası Giriniz'}),
            'security_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Güvenlik Kodu Giriniz'}),
            'expiry_month': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Son Kullanma Tarihi (Ay) Giriniz', 'min': 1, 'max': 12}),
            'expiry_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Son Kullanma Tarihi (Yıl) Giriniz', 'min': timezone.now().year % 100, 'max': 99}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ödeme Tutarı Giriniz'}),
            'amount_write': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ödeme Tutarını Yazı İle Giriniz'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['buyer_select'].initial = self.instance.buyer

        # Zorunlu alanları belirt
        required_fields = [
            'date', 'bank', 'owner', 'card_number', 'security_code',
            'expiry_month', 'expiry_year', 'amount', 'amount_write', 'currency'
        ]
        
        for field_name in required_fields:
            self.fields[field_name].required = True

    def clean(self):
        cleaned_data = super().clean()
        buyer = cleaned_data.get('buyer_select')
        customer_name = cleaned_data.get('customer_name')
        phone = cleaned_data.get('phone')
        address = cleaned_data.get('address')
        customer_choice = self.data.get('customer_choice')

        # Eğer müşteri seçiliyse, ilgili alanları otomatik doldur ve hata ekleme
        if buyer:
            cleaned_data['customer_name'] = buyer.name
            cleaned_data['phone'] = buyer.phone
            cleaned_data['address'] = buyer.address
            self.instance.customer_name = buyer.name
            self.instance.phone = buyer.phone
            self.instance.address = buyer.address
            # Hataları temizle
            if 'customer_name' in self._errors:
                del self._errors['customer_name']
            if 'phone' in self._errors:
                del self._errors['phone']
            if 'address' in self._errors:
                del self._errors['address']
        else:
            # Elle girişte bu alanlar zorunlu
            if not customer_name:
                self.add_error('customer_name', 'Müşteri adı zorunludur.')
            if not phone:
                self.add_error('phone', 'Telefon numarası zorunludur.')
            if not address:
                self.add_error('address', 'Adres zorunludur.')

        # Kart ve diğer alanlar için mevcut zorunluluklar
        card_number = cleaned_data.get('card_number')
        security_code = cleaned_data.get('security_code')
        expiry_month = cleaned_data.get('expiry_month')
        expiry_year = cleaned_data.get('expiry_year')
        owner = cleaned_data.get('owner')
        bank = cleaned_data.get('bank')
        amount = cleaned_data.get('amount')
        amount_write = cleaned_data.get('amount_write')
        date = cleaned_data.get('date')
        currency = cleaned_data.get('currency')

        if not card_number:
            self.add_error('card_number', 'Kart numarası zorunludur.')
        if not security_code:
            self.add_error('security_code', 'Güvenlik kodu zorunludur.')
        if not expiry_month:
            self.add_error('expiry_month', 'Son kullanma ayı zorunludur.')
        if not expiry_year:
            self.add_error('expiry_year', 'Son kullanma yılı zorunludur.')
        if not owner:
            self.add_error('owner', 'Kart sahibi zorunludur.')
        if not bank:
            self.add_error('bank', 'Banka adı zorunludur.')
        if not amount:
            self.add_error('amount', 'Ödeme tutarı zorunludur.')
        if not amount_write:
            self.add_error('amount_write', 'Yazıyla tutar zorunludur.')
        if not date:
            self.add_error('date', 'Tarih zorunludur.')
        if not currency:
            self.add_error('currency', 'Para birimi zorunludur.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('buyer_select'):
            buyer = self.cleaned_data['buyer_select']
            instance.buyer = buyer
            instance.customer_name = buyer.name
            instance.phone = buyer.phone
            instance.address = buyer.address
        
        # Varsayılan şirketi ayarla
        if not instance.company_id:
            instance.company_id = 1  # Varsayılan şirket ID'si
        
        if commit:
            instance.save()
        return instance

class OfferForm(forms.ModelForm):
    buyer_select = forms.ModelChoiceField(
        queryset=Buyer.objects.all(),
        required=False,
        label="Mevcut Müşteriden Seç",
        widget=forms.Select(attrs={'class': 'selectinput form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['valid_until'].initial = timezone.now().date() + timedelta(days=30)
            beklemede_status = OfferStatus.objects.get(name='Beklemede')
            self.fields['status'].initial = beklemede_status

        # Mevcut müşteriyle eşleşiyorsa buyer_select initial'ı ayarla
        if self.instance and self.instance.pk:
            try:
                buyer = Buyer.objects.get(name=self.instance.institution)
                self.fields['buyer_select'].initial = buyer.pk
            except Buyer.DoesNotExist:
                self.fields['buyer_select'].initial = None

        # Tüm alanlara form-control sınıfını ekle
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'selectinput form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        
        # Tarih alanları için özel widget ayarları
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d')
        self.fields['valid_until'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d')
        
        # Placeholder'ları ayarla
        self.fields['institution'].widget.attrs.update({'placeholder': 'Firma/Kurum Adı Giriniz'})
        self.fields['department'].widget.attrs.update({'placeholder': 'Departman Giriniz'})
        self.fields['attention'].widget.attrs.update({'placeholder': 'İlgili Kişi Giriniz'})
        # self.fields['unit'].widget.attrs.update({'placeholder': 'Birim Giriniz'})  # KALDIRILDI
        
        # Institution alanını opsiyonel yap
        self.fields['institution'].required = False

    class Meta:
        model = Offer
        fields = [
            'date',
            'valid_until',
            'institution',
            'department',
            'attention',
            'status',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'valid_until': forms.DateInput(attrs={'type': 'date'}),
        }

class OfferItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'selectinput form-control'})
        self.fields['custom_product_name'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Ürün Adı Giriniz'})
        self.fields['unit'].widget.attrs.update({'class': 'selectinput form-control', 'placeholder': 'Birim'})
        self.fields['quantity'].widget.attrs.update({'class': 'numberinput form-control', 'placeholder': 'Miktar'})
        self.fields['unit_price'].widget.attrs.update({'class': 'numberinput form-control', 'placeholder': 'Birim Fiyat'})
        self.fields['currency'].widget.attrs.update({'class': 'selectinput form-control', 'placeholder': 'Para Birimi'})
        self.fields['tax_rate'].widget.attrs.update({'class': 'selectinput form-control', 'placeholder': 'KDV Oranı'})

        # Para birimi dropdown'unda sadece sembol gözüksün ve TRY, USD, EUR en üstte olsun
        priority_codes = ['TRY', 'USD', 'EUR']
        self.fields['currency'].queryset = Currency.objects.annotate(
            priority=Case(
                When(code='TRY', then=Value(0)),
                When(code='USD', then=Value(1)),
                When(code='EUR', then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).order_by('priority', 'name')
        self.fields['currency'].label_from_instance = lambda obj: f"{obj.symbol} - {obj.code}"

    def clean_unit_price(self):
        value = self.cleaned_data.get('unit_price')
        if isinstance(value, str):
            value = value.replace(',', '.')
        return value

    class Meta:
        model = OfferItem
        fields = ['product', 'custom_product_name', 'unit', 'quantity', 'unit_price', 'currency', 'tax_rate']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'unit_price': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
        }

# Formset tanımlaması
OfferItemFormSet = forms.inlineformset_factory(
    Offer,
    OfferItem,
    form=OfferItemForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True
)

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = [
            'number',
            'date',
            'start_date',
            'end_date',
            'institution',
            'department',
            'authorized_person',
            'contract_type',
            'status',
            'payment_type',
            'installment_count',
            'advance_amount',
            'description',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 12}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.DateInput) and not isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control'})
        # Varsayılan tarihleri ayarla
        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()
            self.fields['start_date'].initial = timezone.now().date()
            self.fields['end_date'].initial = timezone.now().date()
        # Açıklama alanı için placeholder
        self.fields['description'].widget.attrs.update({'placeholder': 'Sözleşme açıklama ve maddeleri...'})
        
    def clean(self):
        cleaned_data = super().clean()
        payment_type = cleaned_data.get('payment_type')
        installment_count = cleaned_data.get('installment_count')

        # payment_type bir PaymentType nesnesi, adı .name ile gelir
        payment_type_name = getattr(payment_type, 'name', None)
        if payment_type_name and payment_type_name.startswith('Taksit'):
            if not installment_count:
                self.add_error('installment_count', 'Taksitli ödemede taksit sayısı zorunludur.')
        return cleaned_data

class ContractItemForm(forms.ModelForm):
    class Meta:
        model = ContractItem
        fields = ['product', 'custom_product_name', 'unit', 'quantity', 'unit_price', 'currency', 'tax_rate']
        widgets = {
            'custom_product_name': forms.TextInput(attrs={'placeholder': 'Ürün Adı (Elle)'}),
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'unit_price': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        # Para birimi dropdown'unda sadece sembol ve kod gözüksün, TRY, USD, EUR en üstte olsun
        priority_codes = ['TRY', 'USD', 'EUR']
        self.fields['currency'].queryset = Currency.objects.annotate(
            priority=Case(
                When(code='TRY', then=Value(0)),
                When(code='USD', then=Value(1)),
                When(code='EUR', then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).order_by('priority', 'name')
        self.fields['currency'].label_from_instance = lambda obj: f"{obj.symbol} - {obj.code}"
        
ContractItemFormSet = forms.inlineformset_factory(
    Contract,
    ContractItem,
    form=ContractItemForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True
)

class ContractInstallmentForm(forms.ModelForm):
    class Meta:
        model = ContractInstallment
        fields = ['number', 'amount', 'date', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.TextInput(attrs={'placeholder': 'Not (isteğe bağlı)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

ContractInstallmentFormSet = forms.inlineformset_factory(
    Contract,
    ContractInstallment,
    form=ContractInstallmentForm,
    extra=0,
    can_delete=False,
    min_num=0,
    validate_min=False
)