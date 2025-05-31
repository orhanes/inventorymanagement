from django.contrib import admin
from .models import (Supplier, Buyer, PurchaseBill, PurchaseItem,PurchaseBillDetails, SaleBill, SaleItem, SaleBillDetails, Delivery, DeliveryBill,
                     Receipt, ReceiptPayment, ReceiptBill, MailOrder, MailOrderBill, Country, City, County, Bank, Offer, OfferItem, OfferBill)


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
admin.site.register(Offer)
admin.site.register(OfferItem)
admin.site.register(OfferBill)

@admin.register(ReceiptPayment)
class ReceiptPaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'receipt', 'payment_method', 'amount', 'currency', 'date', 'description']
    search_fields = ['receipt__number', 'description']
    list_filter = ['payment_method', 'currency', 'date']


