from django.db import models
from inventory.models import Stock
from decimal import *
from common.models import (TaxRates, AddressType, Company, Department, Position, Bank, Currency, 
                           OfferStatus, ContractType, ContractStatus, Unit, PaymentType, PaymentMethod,
                           DeliveryType, DeliveryCompany, VehicleType)
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

def validate_file_size(value):
    if value.size > 5 * 1024 * 1024:
        raise ValidationError("Resim boyutu 5MB'den büyük olamaz.")

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ülke'
        verbose_name_plural = 'Ülkeler'
        

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Şehir'
        verbose_name_plural = 'Şehirler'
       

class County(models.Model):
    name = models.CharField(max_length=120, verbose_name='İlçe Adı')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'İlçe'
        verbose_name_plural = 'İlçeler'


#Tedarikçiler
class Supplier(models.Model):
    
    id = models.AutoField(primary_key=True, verbose_name='Tedarikçi ID')
    image = models.ImageField(
        upload_to='supplier_images/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name='Tedarikçi Logosu',
        help_text='Tedarikçi için bir logo yükleyin',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_file_size
        ]
    )
    name = models.CharField(max_length=150, verbose_name='Tedarikçi Adı')
    country_code = models.CharField(max_length=3, blank=True, null=True, verbose_name='Ülke Kodu')
    phone = models.CharField(max_length=10, unique=True, verbose_name='Telefon')
    fax = models.CharField(max_length=10, blank=True, null=True, verbose_name='Fax')
    address_type = models.ForeignKey(AddressType, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Adres Tipi')
    address = models.CharField(max_length=200, verbose_name='Adres')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name='Ülke Adı')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name='Şehir Adı')
    county = models.ForeignKey(County, on_delete=models.CASCADE, blank=True, null=True, verbose_name='İlçe')
    web = models.CharField(max_length=220, verbose_name='Web Adresi')
    representative = models.CharField(max_length=220, verbose_name='Temsilci')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Departmanı')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Görevi')
    mobile_phone = models.CharField(max_length=20, verbose_name='Cep Telefonu')
    email = models.EmailField(max_length=254, unique=True, verbose_name='E-Mail')
    tax_id = models.PositiveIntegerField(max_length=10, verbose_name='Vergi Kimlik Numarası')
    tax_administration = models.CharField(max_length=220, verbose_name='Vergi Dairesi')
    kep_address = models.CharField(max_length=220, verbose_name='KEP Adresi')
    bank_name = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Banka Adı')
    iban_no = models.CharField(max_length=32, verbose_name='IBAN Numarası')
    branch_code = models.PositiveIntegerField(max_length=12, verbose_name='Şube Kodu')
    account_number = models.PositiveIntegerField(max_length=12, verbose_name='Hesap Numarası')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    class Meta: 
         verbose_name='Tedarikçi'
         verbose_name_plural='Tedarikçiler'

    def __str__(self):
        return self.name
    
#Müşteriler
class Buyer(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Müşteri ID')
    image = models.ImageField(
        upload_to='buyer_images/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name='Müşteri Logosu',
        help_text='Müşteri için bir logo yükleyin',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_file_size
        ]
    )
    name = models.CharField(max_length=120, verbose_name='Müşteri Adı')
    country_code = models.CharField(max_length=3, blank=True, null=True, verbose_name='Ülke Kodu')
    phone = models.CharField(max_length=10, verbose_name='Telefon', blank=True, null=True)
    fax = models.CharField(max_length=10, blank=True, null=True, verbose_name='Fax')
    address_type = models.ForeignKey(AddressType, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Adres Tipi')
    address = models.CharField(max_length=220, verbose_name='Adres')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name='Ülke Adı')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name='Şehir Adı')
    county = models.ForeignKey(County, on_delete=models.CASCADE, blank=True, null=True, verbose_name='İlçe')
    web = models.CharField(max_length=220, verbose_name='Web Adresi')
    representative = models.CharField(max_length=220, verbose_name='Temsilci')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Departmanı')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Görevi')
    mobile_phone = models.CharField(max_length=20, verbose_name='Cep Telefonu')
    email = models.EmailField(max_length=254, verbose_name='E-Mail', blank=True, null=True)
    tax_id = models.CharField(max_length=10, verbose_name='Vergi Kimlik Numarası')
    tax_administration = models.CharField(max_length=220, verbose_name='Vergi Dairesi')
    kep_address = models.CharField(max_length=220, verbose_name='KEP Adresi')
    bank_name = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Banka Adı')
    iban_no = models.CharField(max_length=32, verbose_name='IBAN Numarası')
    branch_code = models.CharField(max_length=12, verbose_name='Şube Kodu')
    account_number = models.CharField(max_length=50, verbose_name='Hesap Numarası')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Müşteri'
        verbose_name_plural = 'Müşteriler'

#Satınalma Formu
class PurchaseBill(models.Model):
    billno = models.AutoField(primary_key=True, verbose_name='Form No')
    year = models.PositiveIntegerField(editable=False, verbose_name='Yıl')
    sequence = models.PositiveIntegerField(editable=False, verbose_name='Sıra No')
    time = models.DateTimeField(auto_now=True, verbose_name='Tarih')
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, verbose_name='Tedarikçi', related_name='purchasesupplier')

    class Meta: 
         verbose_name='Satınalma Faturası'
         verbose_name_plural='Satınalma Faturaları'

    def __str__(self):
        return f"{self.year} / {str(self.sequence).zfill(4)}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Yeni kayıt oluşturuluyorsa
            from django.utils import timezone
            current_year = timezone.now().year
            
            # O yıla ait son kaydı bul ve sıra numarasını ayarla
            last_bill = PurchaseBill.objects.filter(year=current_year).order_by('sequence').last()
            next_sequence = 1
            if last_bill:
                next_sequence = last_bill.sequence + 1
            
            # Yıl ve sıra numarasını kaydet
            self.year = current_year
            self.sequence = next_sequence
        
        super().save(*args, **kwargs)

    def get_items_list(self):
        return PurchaseItem.objects.filter(billno=self)

    def get_total_price(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total += item.totalprice
        return total
    
    def get_total_tax_amount(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total += item.calculate_tax_amount()
        return total

    def get_total_with_tax(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total += item.total_with_tax
        return total

#Satın Alınan Ürünler
class PurchaseItem(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasebillno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='purchaseitem')
    quantity = models.IntegerField(default=1, verbose_name='Miktar')
    perprice = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Birim Fiyat')
    totalprice = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Toplam Fiyat')
    tax_rate = models.ForeignKey(TaxRates, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Vergi Oranı')
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Vergi Tutarı',blank=True, null=True)
    total_with_tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Vergiler Daihl Tutar', blank=True, null=True)
    waybill_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='İrsaliye No')    
    waybill_date = models.DateField(verbose_name='İrsaliye Tarihi', blank=True, null=True)
    due_date = models.DateField(verbose_name='Vade Tarihi', blank=True, null=True)

    class Meta:
        verbose_name = 'Satın Alma Kalemi'
        verbose_name_plural = 'Satın Alma Kalemleri'

    def __str__(self):
        return f"{self.billno.billno} - {self.stock.name}"

    def get_tax_rate_display(self):
        if self.tax_rate:
            return self.tax_rate.rate
        return 0

    # KDV Tutarı Hesaplama
    def calculate_tax_amount(self):
        if self.tax_rate is not None:
            tax_percentage = float(self.tax_rate.rate) / 100
            return float(self.totalprice) * tax_percentage
        return 0  # If tax_rate is not set, return 0

    # KDV'li Toplam tutar Hesaplama
    def save(self, *args, **kwargs):
        self.tax_amount = Decimal(self.calculate_tax_amount())
        self.total_with_tax = Decimal(self.totalprice + self.tax_amount)
        super().save(*args, **kwargs)


#Satın Alma Fatura Detayları
class PurchaseBillDetails(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasedetailsbillno')
    
    po = models.CharField(max_length=50, blank=True, null=True, verbose_name='Satınalma Formu')
    total = models.CharField(max_length=50, blank=True, null=True, verbose_name='Toplam')
    
    def __str__(self):
        return "Fatura No: " + str(self.billno.billno)
    

    class Meta: 
         verbose_name='Satınalma Form Detayı'
         verbose_name_plural='Satınalma Form Detayları'

#Satış Formu
class SaleBill(models.Model):
    billno = models.AutoField(primary_key=True, verbose_name='Form No')
    year = models.PositiveIntegerField(editable=False, verbose_name='Yıl')
    sequence = models.PositiveIntegerField(editable=False, verbose_name='Sıra No')
    time = models.DateTimeField(auto_now=True, verbose_name='Tarih')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Müşteri', related_name='salebuyer')

    class Meta: 
         verbose_name='Satış Formu'
         verbose_name_plural='Satış Formları'

    def __str__(self):
        return f"{self.year} / {str(self.sequence).zfill(4)}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Yeni kayıt oluşturuluyorsa
            from django.utils import timezone
            current_year = timezone.now().year
            
            # O yıla ait son kaydı bul ve sıra numarasını ayarla
            last_bill = SaleBill.objects.filter(year=current_year).order_by('sequence').last()
            next_sequence = 1
            if last_bill:
                next_sequence = last_bill.sequence + 1
            
            # Yıl ve sıra numarasını kaydet
            self.year = current_year
            self.sequence = next_sequence
        
        super().save(*args, **kwargs)

    def get_items_list(self):
        return SaleItem.objects.filter(billno=self)
        
    def get_total_price(self):
        saleitems = SaleItem.objects.filter(billno=self)
        total = 0
        for item in saleitems:
            total += item.totalprice
        return total

    def get_total_tax_amount(self):
        saleitems = SaleItem.objects.filter(billno=self)
        total = 0
        for item in saleitems:
            total += item.calculate_tax_amount()
        return total

    def get_total_with_tax(self):
        saleitems = SaleItem.objects.filter(billno=self)
        total = 0
        for item in saleitems:
            total += item.total_with_tax
        return total

#Satılan Ürün
class SaleItem(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete = models.CASCADE, related_name='salebillno', null=True, blank=True)
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='saleitem')
    quantity = models.IntegerField(default=1, verbose_name='Miktar')
    perprice = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Birim Fiyat')
    totalprice = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Toplam Fiyat')
    tax_rate = models.ForeignKey(TaxRates, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Vergi Oranı')
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Vergi Tutarı',blank=True, null=True)
    total_with_tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Vergiler Daihl Tutar', blank=True, null=True)
    waybill_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='İrsaliye No')    
    waybill_date = models.DateField(verbose_name='İrsaliye Tarihi', blank=True, null=True)
    due_date = models.DateField(verbose_name='Vade Tarihi', blank=True, null=True)
    custom_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Elle Girilen Satış Kalemi")

    class Meta:
        verbose_name = 'Satış Kalemi'
        verbose_name_plural = 'Satış Kalemleri'

    def __str__(self):
        billno_str = self.billno.billno if self.billno and hasattr(self.billno, 'billno') else "-"
        stock_str = self.stock.name if self.stock else (self.custom_name or "-")
        return f"{billno_str} - {stock_str}"
    
    def get_tax_rate_display(self):
        if self.tax_rate:
            return self.tax_rate.rate
        return 0

    # KDV Tutarı Hesaplama
    def calculate_tax_amount(self):
        if self.tax_rate is not None:
            tax_percentage = float(self.tax_rate.rate) / 100
            return float(self.totalprice) * tax_percentage
        return 0  # If tax_rate is not set, return 0

    # KDV'li Toplam tutar Hesaplama
    def save(self, *args, **kwargs):
        self.tax_amount = Decimal(self.calculate_tax_amount())
        self.total_with_tax = Decimal(self.totalprice + self.tax_amount)
        super().save(*args, **kwargs)

#Satış Formu Detayları
class SaleBillDetails(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete = models.CASCADE, related_name='saledetailsbillno')
    po = models.CharField(max_length=50, blank=True, null=True, verbose_name='Satış Emri')
    total = models.CharField(max_length=50, blank=True, null=True, verbose_name='Toplam')

    class Meta: 
         verbose_name='Satış Faturası Detayı'
         verbose_name_plural='Satış Faturası Detayları'

    def __str__(self):
        return "Fatura No: " + str(self.billno.billno)

# Nakliye
class Delivery(models.Model):
     # Ortak alanlar
    id = models.AutoField(primary_key=True, verbose_name='Nakliye ID')
    year = models.PositiveIntegerField(editable=False, verbose_name='Yıl')
    sequence = models.PositiveIntegerField(editable=False, verbose_name='Sıra No')
    delivery_number = models.CharField(max_length=120, verbose_name='Nakliye Form Numarası', unique=True)
    delivery_type = models.ForeignKey(DeliveryType, on_delete=models.CASCADE, verbose_name='Nakliye Türü')
    sale_item = models.ForeignKey(SaleItem, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True, verbose_name='Adres')
    billno = models.CharField(max_length=120, blank=True, null=True, verbose_name='Fiş No')
    deliverer = models.CharField(max_length=120, blank=True, null=True, verbose_name='Teslim Eden')
    description = models.CharField(max_length=300, blank=True, null=True, verbose_name='Not')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    status = models.CharField(
        max_length=20,
        choices=[
            ('BEKLEMEDE', 'Beklemede'),
            ('YOLDA', 'Yolda'),
            ('TESLİM EDİLDİ', 'Teslim Edildi'),
            ('İPTAL', 'İptal'),
        ],
        default='BEKLEMEDE',
        verbose_name='Durum'
    )
    sending_date = models.DateField(null=True, blank=True, verbose_name='Gönderim Tarihi')
    estimated_delivery_date = models.DateField(null=True, blank=True, verbose_name='Tahmini Teslimat Tarihi')
    actual_delivery_date = models.DateField(null=True, blank=True, verbose_name='Gerçekleşen Teslimat Tarihi')
    waybill_number = models.CharField(max_length=120, blank=True, null=True, verbose_name='İrsaliye Numarası')
    
    # Kargo/Posta için
    tracking_number = models.CharField(max_length=120, blank=True, null=True, verbose_name='Takip Numarası')
    delivery_company = models.ForeignKey(DeliveryCompany, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Nakliye Firması')
    
    # Araç/Kurye için
    courier_name = models.CharField(max_length=120, blank=True, null=True, verbose_name='Şoför/Kurye Adı')
    courier_id = models.CharField(max_length=11, blank=True, null=True, verbose_name='T.C. Kimlik No')
    courier_number = models.CharField(max_length=11, blank=True, null=True, verbose_name='Şoför/Kurye Numarası')
    courier_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='Telefon')
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Araç Türü')
    vehicle_plate = models.CharField(max_length=20, blank=True, null=True, verbose_name='Araç Plakası')
    explanation = models.CharField(max_length=120, blank=True, null=True, verbose_name='İzahat')
    tonage = models.BooleanField(default=False, blank=True, null=True, verbose_name='Tonajdan Sorumluyuz')
    analysed = models.BooleanField(default=False, blank=True, null=True, verbose_name='Analizli S-420')
    
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Yeni kayıt oluşturuluyorsa
            from django.utils import timezone
            current_year = timezone.now().year
            
            # O yıla ait son kaydı bul ve sıra numarasını ayarla
            last_delivery = Delivery.objects.filter(year=current_year).order_by('sequence').last()
            next_sequence = 1
            if last_delivery:
                next_sequence = last_delivery.sequence + 1
            
            # Yıl ve sıra numarasını kaydet
            self.year = current_year
            self.sequence = next_sequence
            self.delivery_number = f"{current_year}/{str(next_sequence).zfill(4)}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.delivery_number

    class Meta:
        verbose_name = 'Nakliye'
        verbose_name_plural = 'Nakliyeler'
        ordering = ['-year', '-sequence']

class DeliveryBill(models.Model):
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, primary_key=True, related_name='bill')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Firma', default=1, blank=True, null=True)
    
    class Meta: 
         verbose_name='Malzeme Talep Fişi'
         verbose_name_plural='Malzeme Talep Fişleri'

    def __str__(self):
        return f"Form No: {self.delivery.delivery_number}"


# Tahsilat Makbuzu
class Receipt(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Makbuz ID')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Firma', default=1)
    number = models.CharField(max_length=50, verbose_name='Makbuz Numarası', unique=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateField(verbose_name='Tarih')
    collector = models.CharField(max_length=220, verbose_name='Tahsil Eden')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, verbose_name='Ödeme Yöntemi', default=1)
    payment_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ödeme Toplamı', default=0)
    payment_handwrite = models.CharField(max_length=220, verbose_name='Tutar Yazı ile', blank=True, null=True)
    
    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        if not self.number:
            from datetime import datetime
            prefix = 'RC-'
            date_str = datetime.now().strftime('%Y%m%d')
            last_receipt = Receipt.objects.filter(number__startswith=f'{prefix}{date_str}').order_by('-id').first()
            next_id = (last_receipt.id + 1) if last_receipt else 1
            new_number = f"{prefix}{date_str}-{next_id:04d}"
            while Receipt.objects.filter(number=new_number).exists():
                next_id += 1
                new_number = f"{prefix}{date_str}-{next_id:04d}"
            self.number = new_number
        super().save(*args, **kwargs)

    def get_total_price(self):
        """Makbuzdaki tüm ödemelerin toplam tutarını hesaplar"""
        return sum(payment.amount for payment in self.payments.all())

    def get_total_price_with_tax(self):
        """Makbuzdaki tüm ödemelerin KDV dahil toplam tutarını hesaplar"""
        return sum(payment.amount for payment in self.payments.all())

    def get_total_tax_amount(self):
        """Makbuzdaki tüm ödemelerin KDV tutarını hesaplar"""
        return 0  # KDV tutarı hesaplanmıyorsa 0 döner

    def get_payment_total(self):
        """Makbuzdaki kaydedilmiş ödeme toplamını döndürür"""
        return f"{self.payment_total:,.2f}"

    def get_currency_symbol(self):
        """Makbuzdaki ilk ödemenin para birimi sembolünü döndürür"""
        first_payment = self.payments.first()
        if first_payment and first_payment.currency:
            return first_payment.currency.symbol
        return '₺'  # Varsayılan para birimi sembolü

    def get_total_cash(self):
        """Nakit ödemelerin toplam tutarını hesaplar"""
        return sum(payment.amount for payment in self.payments.all() 
                  if payment.payment_method.name.lower() == 'nakit')

    def get_total_cheque(self):
        """Çek ödemelerin toplam tutarını hesaplar"""
        return sum(payment.amount for payment in self.payments.all() 
                  if payment.payment_method.name.lower() == 'çek')

    def get_total_bond(self):
        """Senet ödemelerin toplam tutarını hesaplar"""
        return sum(payment.amount for payment in self.payments.all() 
                  if payment.payment_method.name.lower() == 'senet')

    def get_total_creditcard(self):
        """Kredi kartı ödemelerin toplam tutarını hesaplar"""
        return sum(payment.amount for payment in self.payments.all() 
                  if payment.payment_method.name.lower() == 'kredi kartı')

    class Meta:
        verbose_name = 'Tahsilat Makbuzu'
        verbose_name_plural = 'Tahsilat Makbuzları'

class ReceiptPayment(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, verbose_name='Ödeme Yöntemi', default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tutar')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name='Para Birimi', default=1)
    date = models.DateField(verbose_name='Tarih')
    description = models.CharField(max_length=220, verbose_name='Açıklama', blank=True, null=True)
    
    class Meta: 
         verbose_name='Tahsilat Ödemesi'
         verbose_name_plural='Tahsilat Ödemeleri'

    def __str__(self):
        return f"{self.amount} {self.currency} - {self.payment_method}"

class ReceiptBill(models.Model):
    receipt = models.OneToOneField(Receipt, on_delete=models.CASCADE, primary_key=True, related_name='bill')
    
    class Meta: 
         verbose_name='Tahsilat Formu'
         verbose_name_plural='Tahsilat Formları'

    def __str__(self):
        return f"Form No: {self.receipt.id}"

class MailOrder(models.Model):
    number = models.CharField(max_length=50, verbose_name='Mail Order Numarası')
    date = models.DateField(verbose_name='Mail Order Tarihi')
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Müşteri')
    customer_name = models.CharField(max_length=100, verbose_name='Müşteri Adı')
    phone = models.CharField(max_length=20, verbose_name='Telefon')
    address = models.TextField(verbose_name='Adres')
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, verbose_name='Banka')
    owner = models.CharField(max_length=100, verbose_name='Kart Sahibi')
    card_number = models.CharField(max_length=19, verbose_name='Kart Numarası')
    security_code = models.CharField(max_length=4, verbose_name='Güvenlik Kodu')
    expiry_month = models.IntegerField(verbose_name='Son Kullanma Tarihi (Ay)', validators=[MinValueValidator(1), MaxValueValidator(12)])
    expiry_year = models.IntegerField(verbose_name='Son Kullanma Tarihi (Yıl)', validators=[MinValueValidator(0), MaxValueValidator(99)])
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ödeme Tutarı')
    amount_write = models.CharField(max_length=100, verbose_name='Ödeme Tutarı (Yazı İle)')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name='Para Birimi', default=1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Firma')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Kullanıcı')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def save(self, *args, **kwargs):
        if not self.number:
            from datetime import datetime
            prefix = 'MO-'
            date_str = datetime.now().strftime('%Y%m%d')
            last_order = MailOrder.objects.filter(number__startswith=f'{prefix}{date_str}').order_by('-id').first()
            next_id = (last_order.id + 1) if last_order else 1
            new_number = f"{prefix}{date_str}-{next_id:04d}"
            while MailOrder.objects.filter(number=new_number).exists():
                next_id += 1
                new_number = f"{prefix}{date_str}-{next_id:04d}"
            self.number = new_number
            
        if self.buyer:
            self.customer_name = self.buyer.name
            self.address = self.buyer.address
            self.phone = self.buyer.phone
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.number or self.customer_name

    class Meta:
        verbose_name = 'Mail Order'
        verbose_name_plural = 'Mail Orderlar'

class MailOrderBill(models.Model):
    mailorder = models.OneToOneField(MailOrder, on_delete=models.CASCADE, primary_key=True, related_name='bill')
    
    class Meta: 
         verbose_name='Mail Order'
         verbose_name_plural='Mail Orderlar'

    def __str__(self):
        return f"Makbuz No: {self.mailorder.id}"


# TEKLİFLER
class Offer(models.Model):
    number = models.CharField(max_length=20, unique=True, verbose_name="Teklif Numarası", blank=True)
    date = models.DateField(default=timezone.now, verbose_name="Tarih")
    valid_until = models.DateField(verbose_name="Geçerlilik Tarihi", null=True, blank=True)
    institution = models.CharField(max_length=200, verbose_name="Kurum")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Departman")
    attention = models.CharField(max_length=200, verbose_name="İlgili Kişi", null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, verbose_name="Firma")
    status = models.ForeignKey(OfferStatus, on_delete=models.SET_NULL, null=True, verbose_name="Teklif Durumu")
    description = models.TextField(
        verbose_name="Teklif Açıklamaları",
        default="""
            TEKLİF AÇIKLAMALARI:
            - Ürünlerimize %20.00 K.D.V. eklenmiştir.
            - Fiyatlarımız TL bazında peşin ödeme esasına göre düzenlenmiştir.
            - Teklifimizdeki ürünler 2 yıl garanti kapsamındadır.
            - Son ödeme tarihini takip eden 1 hafta içerisinde ödenmeyen faturalar için günlük %3 vade farkı uygulanır.
            - Siparişiniz, yazılı onayınızı takiben hemen işleme alınacaktır. Stokta olmayan ürünler 15 iş günü içerisinde iletilmektedir.
            - Bu teklif ve ekinde sunulan tüm bilgiler, verildiği kurum için özel olarak hazırlanmış olup sadece teklif verilenin kullanımına özeldir. Teklifi veren ve alan dışındaki üçüncü kurum/şahıslara iletilemez.
            """
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.number:
            year = timezone.now().year
            last_offer = Offer.objects.filter(number__startswith=f"{year}/").order_by('-number').first()
            if last_offer and last_offer.number:
                last_number = int(last_offer.number.split('/')[-1])
                self.number = f"{year}/{str(last_number + 1).zfill(4)}"
            else:
                self.number = f"{year}/0001"
        super().save(*args, **kwargs)

    def get_total(self):
        # Her kalemin kendi para birimi olabilir, toplu gösterim için sadece sayısal toplam döner
        return sum([item.get_total() for item in self.items.all()])

    def get_vat_amount(self):
        # Her kalemin kendi KDV oranı olabilir, toplam KDV tutarını döner
        return sum([(item.get_total() * (item.tax_rate.rate / 100)) if item.tax_rate else 0 for item in self.items.all()])

    def get_grand_total(self):
        return self.get_total() + self.get_vat_amount()

    def __str__(self):
        return f"{self.number} - {self.institution}"
    
    class Meta:
        verbose_name = 'Teklif'
        verbose_name_plural = 'Teklifler'
        ordering = ['-number']

class OfferItem(models.Model):
    offer = models.ForeignKey(Offer, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ürün (Stoktan Seç)")
    custom_product_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Ürün Adı (Elle)")
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Birim")
    quantity = models.PositiveIntegerField(verbose_name="Miktar")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Birim Fiyat")
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Para Birimi")
    tax_rate = models.ForeignKey(TaxRates, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="KDV Oranı")
    
    def get_total(self):
        return self.quantity * self.unit_price

    def get_vat_amount(self):
        if self.tax_rate:
            return self.get_total() * (self.tax_rate.rate / 100)
        return 0

    def get_grand_total(self):
        return self.get_total() + self.get_vat_amount()

    def __str__(self):
        return self.product.name if self.product else self.custom_product_name
    
class OfferBill(models.Model):
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE, primary_key=True, related_name='bill')

    class Meta:
        verbose_name = 'Teklif Formu'
        verbose_name_plural = 'Teklif Formları'

    def __str__(self):
        return f"Teklif Form No: {self.offer.number}"
    
    class Meta:
        verbose_name = 'Teklif Formu Kalemi'
        verbose_name_plural = 'Teklif Formu Kalemleri'
      
# SÖZLEŞMELER
class Contract(models.Model):
    number = models.CharField(max_length=20, unique=True, verbose_name="Sözleşme Numarası", blank=True)
    date = models.DateField(default=timezone.now, verbose_name="Tarih")
    start_date = models.DateField(verbose_name="Başlangıç Tarihi", null=True, blank=True)
    end_date = models.DateField(verbose_name="Bitiş Tarihi", null=True, blank=True)
    institution = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kurum")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Departman")
    authorized_person = models.CharField(max_length=200, verbose_name="Yetkili Kişi", null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, verbose_name="Firma")
    contract_type = models.ForeignKey(ContractType, on_delete=models.SET_NULL, null=True, verbose_name="Sözleşme Türü")
    status = models.ForeignKey(ContractStatus, on_delete=models.SET_NULL, null=True, verbose_name="Sözleşme Durumu")
    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ödeme Türü")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    installment_count = models.PositiveSmallIntegerField(default=1, null=True, blank=True, verbose_name="Taksit Sayısı")
    advance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True, verbose_name="Avans Tutarı")
    description = models.TextField(
    verbose_name="Sözleşme Açıklama/Maddeleri",
    default="""
{{ firma_adi }} ile sayfa 1/2'de unvan ve adresi yazılı olan kurum/kuruluş arasında iş bu {{ sozlesme_turu }} sözleşmesi akdedilmiştir. Bundan sonra taraflar {{ firma_adi }} ve müşteri olarak anılacaktır.

A- GENEL ŞARTLAR:
1- {{ firma_adi }} tarafından sözleşmesi yapılmış olan satış 1/2'de tanımlı sözleşme türü, başlangıç tarihi sözleşmenin başlangıç tarihi olarak alınacaktır.
2- Ek servis istendiğinde servis elemanının giderleri müşteri tarafından karşılanacaktır.
3- Mesai saatleri dışında, müşterinin servis talep etmesi durumunda, bu zaman dilimleri içerisinde kurum/kuruluşun açık bulundurulması {{ firma_adi }} servis ekibine uygun çalışma ortamı sağlanması ve gerekiyorsa personel temin edilmesi şarttır. Aksi takdirde servis verilmiş sayılır.
4- {{ firma_adi }} tarafından satışı veya bakımı yapılacak yazılım veya donanımların bakım (garanti) süreleri; sözleşmenin türüne göre yapılacaktır.
5- Satışı yapılmış olan {{ firma_adi }} yazılımları hiçbir şekilde, hiçbir şekilde ve yolla başka bir kurum/kuruluşa verilemez, devredilemez ve kopya edilemez. Bu gibi durumlar {{ firma_adi }} lehine tazminat hakkı doğurur.
6- Veri güvenliğinden {{ firma_adi }} sorumlu değildir. Sorumlu olması için veri güvenliği sözleşmesi yapılmış olması gerekir.

B- SÖZLEŞMEYİ (GARANTİ) İPTAL EDEN DURUMLAR:
1- {{ firma_adi }} personeli haricinde dışarıdan yapılan müdahaleler,
2- {{ firma_adi }} tarafından onaylanmamış parça, donanım veya yazılımların sisteme dahilinde kullanılması.
3- Elektrik tesisatından kaynaklanan problemlerden dolayı oluşabilecek bilgi kayıpları (voltaj değişikliği veya elektrik kesintisi).
4- {{ firma_adi }} onayı olmadan dışarıdan yazılım yüklenmesinden kaynaklanan problemler. Örnek: Virüslerden kaynaklanan bozukluklar.
5- {{ firma_adi }} yazılımlarının kopyalanması veya üçüncü şahıslara devredilmesi.
6- Yazılımların kullanım talimatında belirtilen hususlara ve verilen eğitimlere aykırı işlemler yapılması.
7- Donanımın başka bir yere naklinin {{ firma_adi }}'de bildirilmemesi.
8- Deprem, sel, su baskını gibi doğal afetler sonucu oluşan arızalar.
9- Yangın, terör, hırsızlık, ayaklanma gibi olağanüstü durumlarda kaynaklanan hasarlar.
10- Yedekleme ünitelerinin arızalanması yapılmamış olmasından dolayı kaynaklanan kayıplar.

C- {{ firma_adi }}'nin YÜKÜMLÜLÜKLERİ:
1- İlk satışta onarım ve montaj işlemleri sözleşme başlangıç tarihinden itibaren 1 (bir) yıl süreyle ücretsiz hizmet verilecektir.
2- Yazılım eğitimi ve servisi yapılmış olan yazılımlarda meydana gelebilecek arızalar, müşteri tarafından {{ firma_adi }}'ye bildirildikten sonra mümkün olan en kısa sürede arıza tespit ve çözümü için {{ firma_adi }}. Eğitim destek ve Teknik destek birimleri gerekli işlemi başlatır. (bu işlemler durumun aciliyetine göre uzaktan bağlantı, telefon veya müşteri yerinde servis ile çözülmesini). Bu tip servislerin verilmesi konusunda karar verme yetkisi {{ firma_adi }}'ye aittir.
3- {{ firma_adi }}'nin YÜKÜMLÜLÜKLERİ:
4- {{ firma_adi }} ile yapılan sözleşme türüne göre yılda 1 (bir) kez yazılımlar için geliştirme çalışmaları ve donanımlar için bakım kontrolleri yapar.
4- Telefon ve uzaktan bağlantı ile verilen {{ firma_adi }} destek hizmetlerinden herhangi bir ücret alınmayacaktır.
5- Donanım Sözleşme süresi içerisinde müşteri talebi üzerine gerçekleşebilecek parça ilavesi veya donanım geliştirilmesi gibi durumlar {{ firma_adi }}'ye Teknik servisinde gerçekleştirildiğinde parça ücreti dışında teknik servis ücreti alınmayacaktır.
6- {{ firma_adi }} bilgi sistemlerinde meydana gelebilecek teknolojik gelişmelerden müşteriyi bilgilendirecektir.
7- {{ firma_adi }} yazılımlarında yeni modül eklenmesi gibi değişen bölümlerde müşteriye bilgi bildirilecektir.
8- Teknik destek ve eğitim hizmetleri için ayrıca ek bir ücret talep edilmeyecektir.
9- Müşteri talebi ile yapılacak olan bilgi güncellemeleri, müşteri tarafından yazılı olarak bildirildiği takdirde yapılacaktır.
10- {{ firma_adi }} tarafından yapılan bakım ve onarım işlemlerinde, müşteri tarafından bildirilen arızalar dışında sistemde tespit edilen diğer arızalar da giderilecektir.

D- SÖZLEŞME SÜRESİ İÇİNDE ÜCRETE TABİİ İŞLEMLER:
1- Bakım sözleşmesi dışında kalan işlemler için ücret alınacaktır.
2- {{ firma_adi }} tarafından yapılan bakım ve onarım işlemlerinde, müşteri tarafından bildirilen arızalar dışında sistemde tespit edilen diğer arızalar da giderilecektir.
3- Müşteri tarafından talep edilen ek hizmetler için ayrıca ücret alınacaktır.
4- Sözleşme süresi dışında yapılan bakım ve onarım işlemleri için ayrıca ücret alınacaktır.
5- Sözleşme süresi dışında yapılan yazılım güncellemeleri için ayrıca ücret alınacaktır.
6- Sözleşme süresi dışında yapılan donanım güncellemeleri için ayrıca ücret alınacaktır.
7- Sözleşme süresi dışında yapılan eğitim hizmetleri için ayrıca ücret alınacaktır.
8- Sözleşme süresi dışında yapılan teknik destek hizmetleri için ayrıca ücret alınacaktır.

E- DİĞER HÜKÜMLER:
1- Sözleşme bedeli, sözleşme imzalandıktan sonra {{ firma_adi }}'nin {{ banka_adi }} Bankası {{ sube_adi }} şubesindeki {{ iban_no }} IBAN numaralı hesabına yatırılacaktır.
2- Sözleşme bedelinin ödenmemesi halinde, {{ firma_adi }} tarafından sözleşme bedeline yıllık % 10 gecikme faizi uygulanır.
3- Sözleşme ile ilgili doğabilecek ihtilaflarda Ankara Mahkemeleri ve İcra Daireleri yetkilidir.
4- Sözleşme, iki nüsha olarak düzenlenmiş olup, taraflarca okunup imzalandıktan sonra yürürlüğe girer.
5- Sözleşme süresi sonunda taraflarca yeni bir sözleşme yapılmadığı takdirde, sözleşme kendiliğinden sona erer.
"""
)

    def save(self, *args, **kwargs):
        if self.end_date and self.end_date < timezone.now().date() and self.status.name == "Devam Ediyor":
            expired_status = ContractStatus.objects.get(name="Süresi Doldu")
            self.status = expired_status
        if not self.number:
            year = timezone.now().year
            last_contract = Contract.objects.filter(number__startswith=f"{year}/").order_by('-number').first()
            if last_contract and last_contract.number:
                last_number = int(last_contract.number.split('/')[-1])
                self.number = f"{year}/{str(last_number + 1).zfill(4)}"
            else:
                self.number = f"{year}/0001"
        super().save(*args, **kwargs)

    def get_total(self):
        # Her kalemin kendi para birimi olabilir, toplu gösterim için sadece sayısal toplam döner
        return sum([item.get_total() for item in self.items.all()])

    def get_vat_amount(self):
        # Her kalemin kendi KDV oranı olabilir, toplam KDV tutarını döner
        return sum([(item.get_total() * (item.tax_rate.rate / 100)) if item.tax_rate else 0 for item in self.items.all()])

    def get_grand_total(self):
        return self.get_total() + self.get_vat_amount()

    def __str__(self):
        return f"{self.number} - {self.institution}"
    
    class Meta:
        verbose_name = 'Sözleşme'
        verbose_name_plural = 'Sözleşmeler'
        ordering = ['-number']
        
    @property
    def days_left(self):
        if self.end_date:
            return (self.end_date - date.today()).days
        return None
        
class ContractItem(models.Model):
    contract = models.ForeignKey(Contract, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ürün (Stoktan Seç)")
    custom_product_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Ürün Adı (Elle)")
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Birim")
    quantity = models.PositiveIntegerField(verbose_name="Miktar")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Birim Fiyat")
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Para Birimi")
    tax_rate = models.ForeignKey(TaxRates, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="KDV Oranı")
    
    def get_total(self):
        return self.quantity * self.unit_price

    def get_vat_amount(self):
        if self.tax_rate:
            return self.get_total() * (self.tax_rate.rate / 100)
        return 0

    def get_grand_total(self):
        return self.get_total() + self.get_vat_amount()

    def __str__(self):
        return self.product.name if self.product else self.custom_product_name

class ContractInstallment(models.Model):
    contract = models.ForeignKey(Contract, related_name='installments', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Taksit No")
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Tutar (KDV Dahil)")
    date = models.DateField(blank=True, null=True, verbose_name="Taksit Tarihi")
    note = models.CharField(max_length=200, blank=True, null=True, verbose_name="Not")

    def __str__(self):
        return f"{self.contract.number} - Taksit {self.number}"
    
class ContractBill(models.Model):
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, primary_key=True, related_name='bill')

    def __str__(self):
        return f"Sözleşme Form No: {self.contract.number}"
    
    class Meta:
        verbose_name = 'Sözleşme Formu'
        verbose_name_plural = 'Sözleşme Formları'