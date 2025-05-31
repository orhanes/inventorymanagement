from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name='Firma Adı/Ünvanı')
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True, verbose_name='Firma Logosu')
    address = models.TextField(verbose_name='Firma Adresi')
    phone = models.CharField(max_length=20, verbose_name='Firma Telefonu')
    web = models.URLField(max_length=200, verbose_name='Web Adresi')
    email = models.EmailField(max_length=200, verbose_name='E-posta')
    tax_administration = models.CharField(max_length=200, verbose_name='Vergi Dairesi')
    tax_id = models.CharField(max_length=20, verbose_name='Vergi Kimlik No')
    kep_address = models.CharField(max_length=200, verbose_name='KEP Adresi')
    bank_name = models.CharField(max_length=200, verbose_name='Banka Adı')
    iban_no = models.CharField(max_length=50, verbose_name='IBAN No')
    branch_code = models.CharField(max_length=20, verbose_name='Şube Kodu')
    account_number = models.CharField(max_length=20, verbose_name='Hesap No')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    class Meta:
        verbose_name = 'Firma Bilgisi'
        verbose_name_plural = 'Firma Bilgileri'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name='Departman Adı')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Departman'
        verbose_name_plural = 'Departmanlar'
        ordering = ['name']

    def __str__(self):
        return self.name

class Position(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, verbose_name='Pozisyon Adı')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Pozisyon'
        verbose_name_plural = 'Pozisyonlar'
        ordering = ['name']

    def __str__(self):
        return self.name
    
# Banka Türleri
class BankType(models.Model):
    name = models.CharField(max_length=120, verbose_name='Banka Tipi')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Banka Türü'
        verbose_name_plural = 'Banka Türleri'
        ordering = ['name']
        
    def __str__(self):
	    return self.name
    
# Bankalar
class Bank(models.Model):

    logo = models.ImageField(upload_to='bank_logos/', null=True, blank=True, verbose_name='Banka Logosu')
    bank_type = models.ForeignKey(BankType, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Banka Tipi')
    eft_code = models.CharField(max_length=120, blank=True, null=True, verbose_name='EFT Kodu')
    name = models.CharField(max_length=120, verbose_name='Banka Adı')
    phone = models.CharField(max_length=120, blank=True, null=True, verbose_name='Telefon')
    fax = models.CharField(max_length=120, blank=True, null=True, verbose_name='Fax')
    customer_service = models.CharField(max_length=120, blank=True, null=True, verbose_name='Müşteri Hizmetleri')
    email = models.EmailField(max_length=200, blank=True, null=True, verbose_name='E-posta')
    address = models.TextField(blank=True, null=True, verbose_name='Adres')
    website = models.URLField(max_length=200, blank=True, null=True, verbose_name='Web Sitesi')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Banka'
        verbose_name_plural = 'Bankalar'
        ordering = ['name']
    

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Kategori Adı')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
          verbose_name='Kategori'
          verbose_name_plural='Kategoriler'
          
    def __str__(self):
	    return self.name
 
class SubCategory(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Alt Kategori Adı')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Kategori')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    class Meta:
        verbose_name = 'Alt Kategori'
        verbose_name_plural = 'Alt Kategoriler'

    def __str__(self):
        return self.name
        
class Unit(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Birim Adı')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
          verbose_name='Birim'
          verbose_name_plural='Birimler'
          
    def __str__(self):
	    return self.name

class TaxRates(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Vergi Adı')
    rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Vergi Oranı')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    class Meta:
        verbose_name = 'Vergi Oranı'
        verbose_name_plural = 'Vergi Oranları'
        ordering = ['rate']

    def __str__(self):
        return f"%{self.rate}"

    def get_rate_display(self):
        return f"%{self.rate}"


class AddressType(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Adres Türü')
    description = models.CharField(max_length=100, blank=True, null=True, verbose_name='Açıklama')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Adres Türü'
        verbose_name_plural = 'Adres Türleri'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Currency(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="Para Birimi Adı")  # Örn: Türk Lirası
    code = models.CharField(max_length=10, unique=True, verbose_name="Kodu")  # Örn: TRY, USD, EUR
    symbol = models.CharField(max_length=5, verbose_name="Sembol")  # Örn: ₺, $, €

    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        verbose_name = 'Para Birimi'
        verbose_name_plural = 'Para Birimleri'
        ordering = ['name']
    
class OfferStatus(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Teklif Durumu")  # Örn: Taslak, Gönderildi, Onaylandı, Reddedildi
    color = models.CharField(max_length=20, blank=True, null=True, verbose_name="Renk Kodu")  # (opsiyonel, badge için)
    
    class Meta:
        verbose_name = 'Teklif Durumu'
        verbose_name_plural = 'Teklif Durumları'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class ContractType(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Sözleşme Türü")
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Sözleşme Türü'
        verbose_name_plural = 'Sözleşme Türleri'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class ContractStatus(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Sözleşme Durumu")
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Sözleşme Durumu'
        verbose_name_plural = 'Sözleşme Durumları'
        ordering = ['name']

    def __str__(self):
        return self.name

class PaymentType(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Ödeme Türü")
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Ödeme Türü'
        verbose_name_plural = 'Ödeme Türleri'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class PaymentMethod(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Ödeme Yöntemi")
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Ödeme Yöntemi'
        verbose_name_plural = 'Ödeme Yöntemleri'
        ordering = ['name']

    def __str__(self):
        return self.name

class DeliveryType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nakliye Türü Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    is_deleted = models.BooleanField(default=False, verbose_name="Silindi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Nakliye Türü"
        verbose_name_plural = "Nakliye Türleri"
        ordering = ['name']

    def __str__(self):
        return self.name
    
class DeliveryCompany(models.Model):
    logo = models.ImageField(upload_to='delivery_companies/', null=True, blank=True, verbose_name='Nakliye Firması Logosu')
    name = models.CharField(max_length=50, unique=True, verbose_name='Nakliye Firması')
    phone = models.CharField(max_length=120, blank=True, null=True, verbose_name='Telefon')
    fax = models.CharField(max_length=120, blank=True, null=True, verbose_name='Fax')
    customer_service = models.CharField(max_length=120, blank=True, null=True, verbose_name='Müşteri Hizmetleri')
    email = models.EmailField(max_length=200, blank=True, null=True, verbose_name='E-posta')
    address = models.TextField(blank=True, null=True, verbose_name='Adres')
    website = models.URLField(max_length=200, blank=True, null=True, verbose_name='Web Sitesi')
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    is_deleted = models.BooleanField(default=False, verbose_name="Silindi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    
    class Meta:
        verbose_name = 'Nakliye Firması'
        verbose_name_plural = 'Nakliye Firmaları'
        ordering = ['name']
        
    def __str__(self):
        return self.name

class VehicleType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Araç Türü")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    is_deleted = models.BooleanField(default=False, verbose_name="Silindi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Araç Türü"
        verbose_name_plural = "Araç Türleri"
        ordering = ['name']

    def __str__(self):
        return self.name

class VehicleBrand(models.Model):
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, verbose_name='Araç Türü')
    name = models.CharField(max_length=50, verbose_name='Araç Markası')
    description = models.TextField(verbose_name='Açıklama', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Araç Markası'
        verbose_name_plural = 'Araç Markaları'
        ordering = ['vehicle_type', 'name']
        unique_together = ['vehicle_type', 'name']  # Aynı tip altında aynı marka birden fazla olamaz
        
    def __str__(self):
        return f"{self.vehicle_type.name} - {self.name}"

class VehicleModel(models.Model):
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE, verbose_name='Araç Markası')
    name = models.CharField(max_length=50, verbose_name='Model Adı')
    year_start = models.PositiveIntegerField(verbose_name='Başlangıç Yılı', null=True, blank=True)
    year_end = models.PositiveIntegerField(verbose_name='Bitiş Yılı', null=True, blank=True)
    description = models.TextField(verbose_name='Açıklama', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Araç Modeli'
        verbose_name_plural = 'Araç Modelleri'
        ordering = ['brand', 'name']
        unique_together = ['brand', 'name']  # Aynı marka altında aynı model birden fazla olamaz
        
    def __str__(self):
        return f"{self.brand.vehicle_type.name} {self.brand.name} {self.name}"


