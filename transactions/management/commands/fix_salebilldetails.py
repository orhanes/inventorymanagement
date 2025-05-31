from django.core.management.base import BaseCommand
from transactions.models import SaleBill, SaleBillDetails

class Command(BaseCommand):
    help = 'Eksik SaleBillDetails kayıtlarını otomatik olarak oluşturur.'

    def handle(self, *args, **options):
        count = 0
        for sale in SaleBill.objects.all():
            if not SaleBillDetails.objects.filter(billno=sale).exists():
                SaleBillDetails.objects.create(billno=sale)
                self.stdout.write(self.style.SUCCESS(f'SaleBillDetails oluşturuldu: {sale}'))
                count += 1
        if count == 0:
            self.stdout.write(self.style.WARNING('Tüm SaleBill kayıtlarının detayları zaten mevcut.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Toplam {count} adet SaleBillDetails oluşturuldu.')) 