from django.db import models
    
class Stock(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Ürün ID')
    name = models.CharField(max_length=30, unique=True, verbose_name='Ürün Adı')
    CATEGORY = (('Boyalı Profil', 'Boyalı Profil'), ('Siyah Profil', 'Siyah Profil'), ('Boru', 'Boru'), ('Boyalı Boru', 'Boyalı Boru'), ('Sac', 'Sac'))
    category = models.CharField(max_length=20, choices=CATEGORY, null=True, verbose_name='Kategori')
    UNIT = (('Adet', 'Adet'), ('Paket', 'Paket'), ('Kilogram', 'Kilogram'), ('Metre', 'Metre'))
    unit = models.CharField(max_length=20, choices=UNIT, null=True, verbose_name='Birim')
    quantity = models.IntegerField(default=1, verbose_name='Miktar')
    quantity_box= models.IntegerField(default=0, verbose_name='İç Toplam')
    is_deleted = models.BooleanField(default=False, verbose_name='Silindi')

    class Meta:
          verbose_name='Ürün'
          verbose_name_plural='Ürünler'
          
    def __str__(self):
	    return self.name