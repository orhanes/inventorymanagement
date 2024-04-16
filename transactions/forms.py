from django import forms
from django.forms import formset_factory
from .models import (Supplier, Buyer, PurchaseBill, PurchaseItem, PurchaseBillDetails, SaleBill, SaleItem,SaleBillDetails, Delivery,
                    Receipt, MailOrder, Country, City, County, Department, Position, Bank)
from inventory.models import Stock
from django.forms.widgets import DateInput

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true', 'placeholder':'Birim Fiyat Giriniz'})
        self.fields['tax_rate'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['waybill_no'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'İrsaliye Numarası Giriniz'})
        self.fields['waybill_date'].widget.attrs.update({'class': 'dateinput form-control'})
        self.fields['due_date'].widget.attrs.update({'class': 'dateinput form-control'})

    class Meta:
        model = PurchaseItem
        fields = ['stock', 'quantity', 'perprice', 'tax_rate', 'waybill_no','waybill_date', 'due_date']

# Birden fazla 'PurchaseItemForm' oluşturmak için kullanılan form seti
PurchaseItemFormset = formset_factory(PurchaseItemForm, extra=1)

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
        # self.fields['created_date'].widget.attrs.update({'class': 'textinput form-control'})

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true', 'placeholder':'Birim Fiyat Giriniz'})
        self.fields['tax_rate'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['waybill_no'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'İrsaliye Numarası Giriniz'})
        self.fields['waybill_date'].widget.attrs.update({'class': 'dateinput form-control'})
        self.fields['due_date'].widget.attrs.update({'class': 'dateinput form-control'})
    class Meta:
        model = SaleItem
        fields = ['stock', 'quantity', 'perprice', 'tax_rate', 'waybill_no','waybill_date', 'due_date']

# Birden fazla 'SaleItemForm' oluşturmak için kullanılan form seti
SaleItemFormset = formset_factory(SaleItemForm, extra=1)

# Satış faturasının diğer ayrıntılarını kabul etmek için kullanılan form
class SaleDetailsForm(forms.ModelForm):
    class Meta:
        model = SaleBillDetails
        fields = ['po', 'total']

# Nakliye Formu
class DeliveryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sale_item'].queryset = SaleItem.objects.filter()
        self.fields['sale_item'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['buyer'].queryset = Buyer.objects.filter()
        self.fields['buyer'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['billno'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Fiş Numarası Giriniz'})
        self.fields['explanation'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'İzahat Giriniz'})
        self.fields['courier_name'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Şoför Adı Giriniz'})
        self.fields['courier_id'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Şoför T.C. Kimlik No Giriniz', 'maxlength': '11', 'pattern' : '[0-9]+', 'title' : 'Sadece numerik karakterler'})
        self.fields['courier_phone'].widget.attrs.update({'class': 'textinput form-control', 'autocomplete': 'off', 'placeholder':'Şoför Telefonunu Giriniz', 'pattern':'[0-9]+', 'maxlength': '11', 'title' : 'Sadece numerik karakterler'})
        self.fields['courier_vehicle'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['vehicle_plate'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Araç Plakası Giriniz'})
        
    class Meta:
        model = Delivery
        fields = ['buyer', 'sale_item', 'billno', 'explanation', 'courier_name', 'courier_id', 'courier_phone', 'courier_vehicle', 'vehicle_plate', 'description', 'tonage', 'analysed']
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
        }

       
class ReceiptForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['buyer'].queryset = Buyer.objects.filter()
        self.fields['buyer'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['created_date'].widget.attrs.update({'class': 'dateinput form-control'})
        self.fields['serial_number'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Makbuz No Giriniz'})
        self.fields['payment_method'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['payment_total'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Ödeme Toplamı Giriniz'})
        self.fields['payment_one_payment_type'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['payment_one_date'].widget.attrs.update({'class': 'dateinput form-control'})
        self.fields['payment_one_description'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'1. Ödeme İçin Açıklama Giriniz'})
        self.fields['payment_one_amount'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'1. Ödeme Tutarı Giriniz'})
        self.fields['payment_two_payment_type'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['payment_two_date'].widget.attrs.update({'class': 'dateinput form-control'})
        self.fields['payment_two_description'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'2. Ödeme İçin Açıklama Giriniz'})
        self.fields['payment_two_amount'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'2. Ödeme Tutarı Giriniz'})
        self.fields['payment_three_payment_type'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['payment_three_date'].widget.attrs.update({'class': 'dateinput form-control'})
        self.fields['payment_three_description'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'3. Ödeme İçin Açıklama Giriniz'})
        self.fields['payment_three_amount'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'3. Ödeme Tutarı Giriniz'})
        self.fields['payment_handwrite'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Toplam Tutarı Yazı İle Giriniz'})
        self.fields['collector'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Tahsil Eden Adı/Soyadı Giriniz'})
        
    class Meta:
        model = Receipt
        fields = ['buyer', 'created_date', 'serial_number', 'payment_method', 'payment_total', 'payment_one_payment_type', 'payment_one_date', 'payment_one_description', 'payment_one_amount',
                  'payment_two_payment_type', 'payment_two_date', 'payment_two_description', 'payment_two_amount', 'payment_three_payment_type', 'payment_three_date', 'payment_three_description',
                  'payment_three_amount', 'payment_handwrite', 'collector']

class MailOrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer_name'].widget.attrs.update({'class': 'textinput form-control','placeholder':'Müşteri Adı Soyadı veya Firma Adı Giriniz'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'GSM (Cep) veya Sabit Telefon Giiriniz'})
        self.fields['bank'].queryset = Bank.objects.filter()
        self.fields['bank'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['card_number'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Kredi Kartı Numarası Giriniz'})
        self.fields['expiry_month'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Son Kullanma Tarihi Ay Bilgisi Giriniz'})
        self.fields['expiry_year'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Son Kullanma Tarihi Yıl Bilgisi Giriniz'})
        self.fields['security_code'].widget.attrs.update({'class': 'textinput form-control', 'placeholder': 'Kart Güvenlik Kodu Bilgisi Gİriniz'})
        self.fields['amount'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Ödeme Tutarını Rakamla Giriniz'})     
        self.fields['amount_write'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Ödeme Tutarını Yazıyla Giriniz' }) 
        self.fields['date'].widget.attrs.update({'class': 'dateinput form-control'}) 
        self.fields['owner'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Kart Sahibi Bilgisi Giriniz'})          
                    

    class Meta:
        model = MailOrder
        fields = ['customer_name', 'address', 'phone', 'bank', 'card_number', 'expiry_month', 'expiry_year', 'security_code', 'amount', 'amount_write', 'date', 'owner' ]
        widgets = {
            'address' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4',
                    'placeholder': 'Adres Giriniz'
                }
            )
        }

        

