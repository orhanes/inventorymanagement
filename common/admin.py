from django.contrib import admin
from .models import ( Company,Category, SubCategory, Unit, TaxRates, AddressType, Currency, 
                     OfferStatus, Department, Position, Bank, BankType, ContractType, ContractStatus, 
                     PaymentType, PaymentMethod, DeliveryType, DeliveryCompany, VehicleType, VehicleBrand, 
                     VehicleModel )

admin.site.register(Company)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Unit)
admin.site.register(TaxRates)
admin.site.register(AddressType)
admin.site.register(Currency)
admin.site.register(OfferStatus)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Bank)
admin.site.register(BankType)
admin.site.register(ContractType)
admin.site.register(ContractStatus)
admin.site.register(PaymentType)
admin.site.register(PaymentMethod)
admin.site.register(DeliveryType)
admin.site.register(DeliveryCompany)
admin.site.register(VehicleType)
admin.site.register(VehicleBrand)
admin.site.register(VehicleModel)