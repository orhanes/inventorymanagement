from django.db import models
from common.models import Category, Unit, SubCategory
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
import barcode
from barcode.writer import ImageWriter
from django.contrib.auth import get_user_model

def validate_file_size(value):
    if value.size > 5 * 1024 * 1024:
        raise ValidationError("Resim boyutu 5MB'den büyük olamaz.")

class Stock(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Ürün ID')
    image = models.ImageField(
        upload_to='stock_images/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name='Ürün Resmi',
        help_text='Ürün için bir resim yükleyin',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_file_size
        ]
    )
    name = models.CharField(max_length=30, unique=True, verbose_name='Ürün Adı')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name='Kategori')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, verbose_name='Alt Kategori')
    serial_number = models.CharField(max_length=30, unique=True, blank=True, null=True, verbose_name='Seri Numarası')
    color = models.CharField(max_length=30, blank=True, null=True, verbose_name='Renk')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, verbose_name='Birim')
    quantity = models.IntegerField(default=1, verbose_name='Miktar')
    # quantity_box= models.IntegerField(default=0, blank=True, null=True, verbose_name='İç Toplam')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    brand = models.CharField(max_length=50, blank=True, null=True, verbose_name='Marka')
    model = models.CharField(max_length=50, blank=True, null=True, verbose_name='Model')
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name='Barkod Numarası')
    description = models.TextField(blank=True, null=True, verbose_name='Açıklama')
    min_stock_level = models.IntegerField(default=0, verbose_name='Minimum Stok Seviyesi')
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name='Raf/Konum')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Alış Fiyatı')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Satış Fiyatı')
    expiry_date = models.DateField(blank=True, null=True, verbose_name='Son Kullanma Tarihi')
    warranty_period = models.CharField(max_length=30, blank=True, null=True, verbose_name='Garanti Süresi')
    manufacturer = models.CharField(max_length=100, blank=True, null=True, verbose_name='Üretici')
    supplier = models.ForeignKey('transactions.Supplier', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Tedarikçi')

    class Meta:
          verbose_name='Ürün'
          verbose_name_plural='Ürünler'
          
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Otomatik ve unique barkod üretimi
        if not self.barcode:
            prefix = 'STK-'
            last_id = Stock.objects.all().order_by('-id').first()
            next_id = (last_id.id + 1) if last_id else 1
            new_barcode = f"{prefix}{next_id:06d}"
            # Benzersiz olana kadar artır
            while Stock.objects.filter(barcode=new_barcode).exists():
                next_id += 1
                new_barcode = f"{prefix}{next_id:06d}"
            self.barcode = new_barcode
        super().save(*args, **kwargs)

class StockCard(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='cards', verbose_name='Ürün')
    lot = models.CharField(max_length=30, blank=True, null=True, verbose_name='LOT')
    heat_no = models.CharField(max_length=30, blank=True, null=True, verbose_name='Döküm No')
    quality = models.CharField(max_length=30, blank=True, null=True, verbose_name='Kalite')
    type = models.CharField(max_length=30, blank=True, null=True, verbose_name='Cinsi')
    quantity = models.IntegerField(default=1, verbose_name='Adet')
    length = models.CharField(max_length=20, blank=True, null=True, verbose_name='Boy')
    std = models.CharField(max_length=30, blank=True, null=True, verbose_name='Standart')
    operator = models.CharField(max_length=30, blank=True, null=True, verbose_name='Operatör')
    package_no = models.CharField(max_length=30, blank=True, null=True, verbose_name='Paket No')
    origin = models.CharField(max_length=30, blank=True, null=True, verbose_name='Menşei')
    date = models.DateField(blank=True, null=True, verbose_name='Tarih')
    serial_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Seri No')
    qr_code = models.ImageField(upload_to='stock_qr/', blank=True, null=True, verbose_name='QR Kod')
    barcode_number = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name='Barkod Numarası')
    quality_control = models.CharField(max_length=30, blank=True, null=True, verbose_name='Kalite Kontrol')
    packer = models.CharField(max_length=30, blank=True, null=True, verbose_name='Paketçi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Stok Kartı'
        verbose_name_plural = 'Stok Kartları'

    def __str__(self):
        return f"{self.stock.name} - {self.lot or self.serial_number or self.pk}"

    def get_qr_data(self):
        import json
        data = {
            'serial': self.serial_number,
            'lot': self.lot,
            'product': self.stock.name if self.stock else '',
            'date': self.date.strftime('%Y-%m-%d') if self.date else ''
        }
        return json.dumps(data, ensure_ascii=False)

    def save(self, *args, **kwargs):
        # Otomatik ve unique barkod üretimi
        if not self.barcode_number:
            from datetime import datetime
            prefix = 'CARD-'
            date_str = datetime.now().strftime('%Y%m%d')
            last_card = StockCard.objects.filter(barcode_number__startswith=f'{prefix}{date_str}').order_by('-id').first()
            next_id = (last_card.id + 1) if last_card else 1
            new_barcode = f"{prefix}{date_str}-{next_id:04d}"
            while StockCard.objects.filter(barcode_number=new_barcode).exists():
                next_id += 1
                new_barcode = f"{prefix}{date_str}-{next_id:04d}"
            self.barcode_number = new_barcode

        # QR Kod üretimi
        qr_data = self.get_qr_data()
        if qr_data and not self.qr_code:
            qr_img = qrcode.make(qr_data)
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            file_name = f"qr_{self.serial_number or self.pk}.png"
            self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)

        # Barkod üretimi (Code128, seri no veya lot)
        barcode_data = self.serial_number or self.lot or str(self.pk)
        if barcode_data and not self.barcode:
            CODE128 = barcode.get_barcode_class('code128')
            bar_img = CODE128(barcode_data, writer=ImageWriter())
            buffer = BytesIO()
            bar_img.write(buffer, options={"write_text": False})
            file_name = f"barcode_{barcode_data}.png"
            self.barcode.save(file_name, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

class StockLog(models.Model):
    ACTION_CHOICES = [
        ('read', 'Okuma'),
        ('create', 'Ekleme'),
        ('update', 'Güncelleme'),
        ('delete', 'Silme'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kullanıcı')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ürün')
    stockcard = models.ForeignKey(StockCard, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Stok Kartı')
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Stok Logu'
        verbose_name_plural = 'Stok Logları'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.timestamp.strftime('%d.%m.%Y %H:%M')}"

    
