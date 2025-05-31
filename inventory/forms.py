from django import forms
from .models import Stock, StockCard
from django.forms.widgets import DateInput

class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*',
            'style': 'max-width: 100%; height: auto;'
        })
        self.fields['brand'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Marka Giriniz'})
        self.fields['model'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Model Giriniz'})
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Ürün Adı Giriniz', 'style': 'text-transform: uppercase;'})
        self.fields['category'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['subcategory'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['serial_number'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Seri Numarası Giriniz', 'style': 'text-transform: uppercase;'})
        self.fields['color'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Renk Giriniz', 'style': 'text-transform: uppercase;'})
        self.fields['unit'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
        self.fields['purchase_price'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Alış Fiyatı Giriniz'})
        self.fields['sale_price'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Satış Fiyatı Giriniz'})
        self.fields['location'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Raf/Konum Giriniz'})
        self.fields['min_stock_level'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
        self.fields['expiry_date'].widget = DateInput(attrs={'type': 'date', 'class': 'form-control'})
        self.fields['warranty_period'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Garanti Süresi Giriniz'})
        self.fields['manufacturer'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Üretici Giriniz'})
        self.fields['supplier'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['barcode'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Barkod Numarası Giriniz'})
        self.fields['description'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Açıklama Giriniz', 'rows': 2})
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
        
        
        
    class Meta:
        model = Stock
        fields = [
            'image', 'name', 'category', 'subcategory', 'serial_number', 'color', 'unit', 'quantity',
            'brand', 'model', 'barcode', 'description', 'min_stock_level', 'location', 'is_active',
            'purchase_price', 'sale_price', 'expiry_date', 'warranty_period', 'manufacturer', 'supplier'
        ]

class StockCardForm(forms.ModelForm):
    class Meta:
        model = StockCard
        exclude = ['qr_code', 'barcode', 'created_at', 'updated_at']
        widgets = {
            'barcode_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Barkod Numarası Giriniz'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'stock': forms.Select(attrs={'class': 'form-control'}),
            'lot': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Lot Giriniz'}),
            'heat_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Heat No Giriniz'}),
            'quality': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Kalite Giriniz'}),
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Tür Giriniz'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder':'Miktar Giriniz'}),
            'length': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Uzunluk Giriniz'}),
            'std': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Standart Giriniz'}),
            'operator': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Operatör Giriniz'}),
            'package_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Paket No Giriniz'}),
            'origin': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Üretim Ülkesi Giriniz'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Seri No Giriniz'}),
            'quality_control': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Kalite Kontrol Giriniz'}),
            'packer': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Paketçi Giriniz'}),
        }