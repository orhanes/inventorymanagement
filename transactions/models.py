from django.db import models
from inventory.models import Stock
from decimal import *

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


# Departmanlar
class Department(models.Model):

    name = models.CharField(max_length=120, verbose_name='Departman Adı')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Departman'
        verbose_name_plural = 'Departmanlar'

# Pozisyonlar/Görevler
class Position(models.Model):

    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, verbose_name='Pozisyon Adı')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Pozisyon'
        verbose_name_plural = 'Pozisyonlar'

# Bankalar
class Bank(models.Model):

    name = models.CharField(max_length=120, verbose_name='Banka Adı')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Banka'
        verbose_name_plural = 'Bankalar'


#Tedarikçiler
class Supplier(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Tedarikçi ID')
    name = models.CharField(max_length=150, verbose_name='Tedarikçi Adı')
    phone = models.CharField(max_length=12, unique=True, verbose_name='Telefon')
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
    tax_id = models.PositiveIntegerField(max_length=12, verbose_name='Vergi Kimlik Numarası')
    tax_administration = models.CharField(max_length=220, verbose_name='Vergi Dairesi')
    kep_address = models.CharField(max_length=220, verbose_name='KEP Adresi')
    bank_name = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Banka Adı')
    iban_no = models.CharField(max_length=220, verbose_name='IBAN Numarası')
    branch_code = models.PositiveIntegerField(max_length=12, verbose_name='Şube Kodu')
    account_number = models.PositiveIntegerField(max_length=12, verbose_name='Hesap Numarası')
    created_date = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')

    class Meta: 
         verbose_name='Tedarikçi'
         verbose_name_plural='Tedarikçiler'

    def __str__(self):
        return self.name
    
#Müşteriler
class Buyer(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Müşteri ID')
    name = models.CharField(max_length=120, unique=True, verbose_name='Müşteri Adı')
    phone = models.CharField(max_length=50, verbose_name='Telefon')
    address = models.CharField(max_length=220, verbose_name='Adres')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name='Ülke Adı')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name='Şehir Adı')
    county = models.ForeignKey(County, on_delete=models.CASCADE, blank=True, null=True, verbose_name='İlçe')
    web = models.CharField(max_length=220, verbose_name='Web Adresi')
    representative = models.CharField(max_length=220, verbose_name='Temsilci')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Departmanı')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Görevi')
    mobile_phone = models.CharField(max_length=20, verbose_name='Cep Telefonu')
    email = models.EmailField(max_length=254, unique=True, verbose_name='E-Mail')
    tax_id = models.CharField(max_length=50, verbose_name='Vergi Kimlik Numarası')
    tax_administration = models.CharField(max_length=220, verbose_name='Vergi Dairesi')
    kep_address = models.CharField(max_length=220, verbose_name='KEP Adresi')
    bank_name = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Banka Adı')
    iban_no = models.CharField(max_length=220, verbose_name='IBAN Numarası')
    branch_code = models.CharField(max_length=50, verbose_name='Şube Kodu')
    account_number = models.CharField(max_length=50, verbose_name='Hesap Numarası')
    created_date = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Müşteri'
        verbose_name_plural = 'Müşteriler'

#Satınalma Faturaları
class PurchaseBill(models.Model):
    billno = models.AutoField(primary_key=True, verbose_name='Fatura No')
    time = models.DateTimeField(auto_now=True, verbose_name='Tarih')
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, verbose_name='Tedarikçi', related_name='purchasesupplier')

    class Meta: 
         verbose_name='Satınalma Faturası'
         verbose_name_plural='Satınalma Faturaları'

    def __str__(self):
        return "Fatura No: " + str(self.billno)

    def get_items_list(self):
        return PurchaseItem.objects.filter(billno=self)

    def get_total_price(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total += item.totalprice
        return total
    
#Satın Alınan Ürünler
class PurchaseItem(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasebillno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='purchaseitem')
    quantity = models.IntegerField(default=1, verbose_name='Miktar')
    perprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Birim Fiyat')
    totalprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Toplam Fiyat')
    TAX_CHOICES = ((0, '0'), (8, '8'), (10, '10'), (20, '20'),)
    tax_rate = models.IntegerField(choices=TAX_CHOICES, verbose_name='Vergi Oranı', blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Vergi Tutarı',blank=True, null=True)
    total_with_tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Vergiler Daihl Tutar', blank=True, null=True)
    waybill_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='İrsaliye No')    
    waybill_date = models.DateField(verbose_name='İrsaliye Tarihi', blank=True, null=True)
    due_date = models.DateField(verbose_name='Vade Tarihi', blank=True, null=True)

    class Meta: 
         verbose_name='Ürün'
         verbose_name_plural='Ürünler'
    
    # KDV Tutarı Hesaplama
    def calculate_tax_amount(self):
        if self.tax_rate is not None:
            tax_percentage = float(self.tax_rate) / 100
            return float(self.totalprice) * tax_percentage
        return 0  # If tax_rate is not set, return 0

    def __str__(self):
        return f"Vergi Tutarı: {self.calculate_tax_amount()}"

    # KDV'li Toplam tutar Hesaplama
    def save(self, *args, **kwargs):
        self.tax_amount = Decimal(self.calculate_tax_amount())
        self.total_with_tax = Decimal(self.totalprice + self.tax_amount)
        super().save(*args, **kwargs)


#Satın Alma Fatura Detayları
class PurchaseBillDetails(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasedetailsbillno')
    
    po = models.CharField(max_length=50, blank=True, null=True, verbose_name='Satınalma Emri')
    total = models.CharField(max_length=50, blank=True, null=True, verbose_name='Toplam')
    
    def __str__(self):
        return "Fatura No: " + str(self.billno.billno)
    

    class Meta: 
         verbose_name='Satınalma Fatura Detayı'
         verbose_name_plural='Satınalma Fatura Detayları'

#Satış Faturası
class SaleBill(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Müşteri')
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    tax_id = models.CharField(max_length=10)


    class Meta: 
         verbose_name='Satış Faturası'
         verbose_name_plural='Satış Faturaları'

    def __str__(self):
        return "Fatura No: " + str(self.billno)

    def get_items_list(self):
        return SaleItem.objects.filter(billno=self)
        
    def get_total_price(self):
        saleitems = SaleItem.objects.filter(billno=self)
        total = 0
        for item in saleitems:
            total += item.totalprice
        return total

#Satılan Ürün
class SaleItem(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete = models.CASCADE, related_name='salebillno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='saleitem')
    quantity = models.IntegerField(default=1, verbose_name='Miktar')
    perprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Birim Fiyat')
    totalprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Toplam Fiyat')
    TAX_CHOICES = ((0, '0'), (8, '8'), (10, '10'), (20, '20'),)
    tax_rate = models.IntegerField(choices=TAX_CHOICES, verbose_name='Vergi Oranı', blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Vergi Tutarı',blank=True, null=True)
    total_with_tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Vergiler Daihl Tutar', blank=True, null=True)
    waybill_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='İrsaliye No')    
    waybill_date = models.DateField(verbose_name='İrsaliye Tarihi', blank=True, null=True)
    due_date = models.DateField(verbose_name='Vade Tarihi', blank=True, null=True)

    class Meta: 
         verbose_name='Satılan Ürün'
         verbose_name_plural='Satılan Ürünler'

    def __str__(self):
        return "Fatura No: " + str(self.billno.billno) + ", Ürün = " + self.stock.name
    
    # KDV Tutarı Hesaplama
    def calculate_tax_amount(self):
        if self.tax_rate is not None:
            tax_percentage = float(self.tax_rate) / 100
            return float(self.totalprice) * tax_percentage
        return 0  # If tax_rate is not set, return 0

    def __str__(self):
        return f"Vergi Tutarı: {self.calculate_tax_amount()}"

    # KDV'li Toplam tutar Hesaplama
    def save(self, *args, **kwargs):
        self.tax_amount = Decimal(self.calculate_tax_amount())
        self.total_with_tax = Decimal(self.totalprice + self.tax_amount)
        super().save(*args, **kwargs)

#Satış Faturası
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
    id = models.AutoField(primary_key=True, verbose_name='Nakliye ID')
    sale_item = models.ForeignKey(SaleItem, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, blank=True, null=True)
    billno = models.CharField(max_length=120, verbose_name='Fiş No')
    explanation = models.CharField(max_length=120, verbose_name='İzahat')
    courier_name = models.CharField(max_length=120, verbose_name='Şoför Adı / Soyadı')
    courier_id = models.IntegerField(max_length=11, verbose_name='Şoför T.C. Kimlik No')
    courier_phone = models.CharField(max_length=11, verbose_name='Şoför Telefonu')
    COURIER_VEHICLE_CHOICE = (('Otomobil', 'OTOMOBİL'), ('Kamyonet', 'KAMYONET'), ('Pikap', 'PİKAP'), ('Kamyon', 'KAMYON'), ('Tır', 'TIR'),)
    courier_vehicle = models.CharField(max_length=220, choices=COURIER_VEHICLE_CHOICE, verbose_name='Şoför Aracı')
    vehicle_plate = models.CharField(max_length=20, verbose_name='Şoför Plakası')
    created_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=300, verbose_name='Not')
    tonage = models.BooleanField(default=False, verbose_name='Tonajdan Sorumluyuz')
    analysed = models.BooleanField(default=False, verbose_name='Analizli S-420')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')

    def __str__(self):
        return self.billno

    class Meta:
        verbose_name = 'Nakliye'
        verbose_name_plural = 'Nakliyeler'

class DeliveryBill(models.Model):
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, primary_key=True, related_name='bill')
    
    class Meta: 
         verbose_name='Malzeme Talep Fişi'
         verbose_name_plural='Malzeme Talep Fişleri'

    def __str__(self):
        return f"Fiş No: {self.delivery.billno}"


# Tahsilat Makbuzu
class Receipt(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Makbuz ID')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateField(verbose_name='Tarih')
    serial_number = models.CharField(max_length=10, verbose_name='Seri No')
    PAYMENT_CHOICE = (('Nakit', 'Nakit'), ('Çek', 'Çek'), ('Senet', 'Senet'), ('Kredi Kartı', 'Kredi Kartı'),)
    payment_method = models.CharField(max_length=120, choices=PAYMENT_CHOICE, verbose_name='Ödeme Yöntemi')
    payment_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ödeme Toplamı')
    payment_one_payment_type = models.CharField(max_length=120, choices=PAYMENT_CHOICE, verbose_name='Ödeme 1 Cinsi')
    payment_one_date = models.DateField(verbose_name='Ödeme 1 Tarihi')
    payment_one_description = models.CharField(max_length=220, verbose_name='Ödeme 1 Açıklama')
    payment_one_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ödeme 1 Tutarı')
    payment_two_payment_type = models.CharField(max_length=120, choices=PAYMENT_CHOICE, verbose_name='Ödeme 2 Cinsi')
    payment_two_date = models.DateField(verbose_name='Ödeme 2 Tarihi')
    payment_two_description = models.CharField(max_length=220, verbose_name='Ödeme 2 Açıklama')
    payment_two_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ödeme 2 Tutarı')
    payment_three_payment_type = models.CharField(max_length=120, choices=PAYMENT_CHOICE, verbose_name='Ödeme 3 Cinsi')
    payment_three_date = models.DateField(verbose_name='Ödeme 3 Tarihi')
    payment_three_description = models.CharField(max_length=220, verbose_name='Ödeme 3 Açıklama')
    payment_three_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ödeme 3 Tutarı')
    payment_handwrite = models.CharField(max_length=220, verbose_name='Tutar Yazı İle')
    collector = models.CharField(max_length=220, verbose_name='Tahsil Eden')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')


    def __str__(self):
        return self.serial_number
    
    # TOPLAM TUTAR HESAPLAMA
    def get_total_price(self):
        return self.payment_one_amount + self.payment_two_amount + self.payment_three_amount
    
    
    def total_cash(self):
        cash_payments = [self.payment_one_amount, self.payment_two_amount, self.payment_three_amount]
        cash_payment_types = [self.payment_one_payment_type, self.payment_two_payment_type, self.payment_three_payment_type]

        total_cash_paid = sum(amount for amount, payment_type in zip(cash_payments, cash_payment_types) if payment_type == 'Nakit')
        return total_cash_paid

        
    def total_cheque(self):
        cheque_payments = [self.payment_one_amount, self.payment_two_amount, self.payment_three_amount]
        cheque_payment_types = [self.payment_one_payment_type, self.payment_two_payment_type, self.payment_three_payment_type]

        total_cheque_paid = sum(amount for amount, payment_type in zip(cheque_payments, cheque_payment_types) if payment_type == 'Çek')
        return total_cheque_paid

    
    def total_bond(self):
        bond_payments = [self.payment_one_amount, self.payment_two_amount, self.payment_three_amount]
        bond_payment_types = [self.payment_one_payment_type, self.payment_two_payment_type, self.payment_three_payment_type]

        total_bond_paid = sum(amount for amount, payment_type in zip(bond_payments, bond_payment_types) if payment_type == 'Senet')
        return total_bond_paid
    
    def total_creditcard(self):
        creditcard_payments = [self.payment_one_amount, self.payment_two_amount, self.payment_three_amount]
        creditcard_payment_types = [self.payment_one_payment_type, self.payment_two_payment_type, self.payment_three_payment_type]

        total_creditcard_paid = sum(amount for amount, payment_type in zip(creditcard_payments, creditcard_payment_types) if payment_type == 'Kredi Kartı')
        return total_creditcard_paid

    class Meta:
        verbose_name = 'Tahsilat Makbuzu'
        verbose_name_plural = 'Tahsilat Makbuzları'

class ReceiptBill(models.Model):
    receipt = models.OneToOneField(Receipt, on_delete=models.CASCADE, primary_key=True, related_name='bill')
    
    class Meta: 
         verbose_name='Tahsilat Makbuzu'
         verbose_name_plural='Tahsilat Makbuzları'

    def __str__(self):
        return f"Makbuz No: {self.receipt.serial_number}"

class MailOrder(models.Model):

     id = models.AutoField(primary_key=True, verbose_name='Mail Order ID')
     customer_name = models.CharField(max_length=220, verbose_name='Müşteri Adı Soyadı / Firma Adı')
     address = models.CharField(max_length=220, verbose_name='Adres')
     phone = models.CharField(max_length=20, verbose_name='Mobil / Sabit Telefon')
     bank = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Banka Adı')
     card_number = models.IntegerField(max_length=16, verbose_name='Kart No')
     expiry_month = models.IntegerField(max_length=10, verbose_name='Son Kullanma Tarihi (Ay)')
     expiry_year = models.IntegerField(max_length=10, verbose_name='Son Kullanma Tarihi (Yıl)')
     security_code = models.IntegerField(max_length=10, verbose_name='Güvenlik Kodu')
     amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ödeme Tutarı (Rakamla)')
     amount_write = models.CharField(max_length=220, verbose_name='Ödeme Tutarı (Yazıyla)')
     date = models.DateField(verbose_name='Ödeme Tarihi')
     owner = models.CharField(max_length=220, verbose_name='Kart Sahibi')
     is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
     
     def __str__(self):
        return self.customer_name

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