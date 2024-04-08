from django.contrib import admin
from .models import (Supplier, Buyer, PurchaseBill, PurchaseItem,PurchaseBillDetails, SaleBill, SaleItem, SaleBillDetails, Delivery, DeliveryBill,
                     Receipt,  ReceiptBill, MailOrder, MailOrderBill, Country, City, County, Department, Position, Bank)


admin.site.register(Supplier)
admin.site.register(Buyer)
admin.site.register(PurchaseBill)
admin.site.register(PurchaseItem)
admin.site.register(PurchaseBillDetails)
admin.site.register(SaleBill)
admin.site.register(SaleItem)
admin.site.register(SaleBillDetails)
admin.site.register(Delivery)
admin.site.register(DeliveryBill)
admin.site.register(Receipt)
admin.site.register(ReceiptBill)
admin.site.register(MailOrder)
admin.site.register(MailOrderBill)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(County)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Bank)



