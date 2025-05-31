from django.urls import path
from django.urls import re_path as url
from . import views

urlpatterns = [


    path('suppliers/', views.SupplierListView.as_view(), name='suppliers-list'),
    path('suppliers/new', views.SupplierCreateView.as_view(), name='new-supplier'),
    path('suppliers/<pk>/edit', views.SupplierUpdateView.as_view(), name='edit-supplier'),
    path('suppliers/<pk>/delete', views.SupplierDeleteView.as_view(), name='delete-supplier'),
    path('supplier/<int:pk>', views.SupplierView.as_view(), name='supplier'),

    path('buyers/', views.BuyerListView.as_view(), name='buyers-list'),
    path('buyers/new', views.BuyerCreateView.as_view(), name='new-buyer'),
    path('buyers/<pk>/edit', views.BuyerUpdateView.as_view(), name='edit-buyer'),
    path('buyers/<pk>/delete', views.BuyerDeleteView.as_view(), name='delete-buyer'),
    path('buyer/<int:pk>', views.BuyerView.as_view(), name='buyer'),

    path('purchases/', views.PurchaseView.as_view(), name='purchases-list'), 
    path('purchases/new', views.SelectSupplierView.as_view(), name='select-supplier'), 
    path('purchases/new/<pk>', views.PurchaseCreateView.as_view(), name='new-purchase'),    
    path('purchases/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),
    path("purchases/<billno>", views.PurchaseBillView.as_view(), name="purchase-bill"),
    path('purchases/edit/<str:billno>/', views.PurchaseUpdateView.as_view(), name='purchase-edit'),

    path('sales/', views.SaleView.as_view(), name='sales-list'),
    path('sales/new', views.SelectBuyerView.as_view(), name='select-buyer'), 
    path('sales/new/<pk>', views.SaleCreateView.as_view(), name='new-sale'),    
    path('sales/<pk>/delete', views.SaleDeleteView.as_view(), name='delete-sale'),
    path("sales/<billno>", views.SaleBillView.as_view(), name="sale-bill"),
    path('sales/edit/<str:billno>/', views.SaleUpdateView.as_view(), name='sale-edit'),

    path('deliveries/', views.DeliveryListView.as_view(), name='deliveries-list'),
    path('deliveries/new', views.DeliveryCreateView.as_view(), name='new-delivery'),
    path('deliveries/<pk>/edit', views.DeliveryUpdateView.as_view(), name='edit-delivery'),
    path('deliveries/<pk>/delete', views.DeliveryDeleteView.as_view(), name='delete-delivery'),
    path('delivery/<id>', views.DeliveryView.as_view(), name='delivery'),
    path('deliveries/bill/<path:billno>/', views.DeliveryBillView.as_view(), name='delivery-bill'),

    path('receipts/', views.ReceiptListView.as_view(), name='receipts-list'),
    path('receipts/new', views.ReceiptCreateView.as_view(), name='new-receipt'),
    path('receipts/<pk>/edit', views.ReceiptUpdateView.as_view(), name='edit-receipt'),
    path('receipts/<pk>/delete', views.ReceiptDeleteView.as_view(), name='delete-receipt'),
    path('receipts/<id>', views.ReceiptView.as_view(), name='receipt'),
    path('receipts/<id>/', views.ReceiptBillView.as_view(), name='receipt-bill'),

    path('mailorders/', views.MailOrderListView.as_view(), name='mailorders-list'),
    path('mailorders/new', views.MailOrderCreateView.as_view(), name='new-mailorder'),
    path('mailorders/<pk>/edit', views.MailOrderUpdateView.as_view(), name='edit-mailorder'),
    path('mailorders/<pk>/delete', views.MailOrderDeleteView.as_view(), name='delete-mailorder'),
    path('mailorders/<id>', views.MailOrderView.as_view(), name='mailorder'),
    path('mailorders/<id>/', views.MailOrderBillView.as_view(), name='mailorder-bill'),
    
    path('offers/', views.OfferListView.as_view(), name='offers-list'),
    path('offers/new', views.OfferCreateView.as_view(), name='new-offer'),
    path('offers/<pk>/edit', views.OfferUpdateView.as_view(), name='edit-offer'),
    path('offers/<pk>/delete', views.OfferDeleteView.as_view(), name='delete-offer'),
    path('offers/<id>', views.OfferDetailView.as_view(), name='offer'),
    path('offers/<id>/', views.OfferBillView.as_view(), name='offer-bill'),
    path('offers/<int:pk>/cancel/', views.cancel_offer, name='cancel-offer'),
    
    path('contracts/', views.ContractListView.as_view(), name='contract-list'),
    path('contracts/new', views.ContractCreateView.as_view(), name='new-contract'),
    path('contracts/<int:pk>/edit/', views.ContractUpdateView.as_view(), name='edit-contract'),
    path('contracts/<int:pk>/delete/', views.ContractDeleteView.as_view(), name='delete-contract'),
    path('contracts/<int:id>/', views.ContractDetailView.as_view(), name='contract'),
    path('contracts/<int:id>/bill/', views.ContractBillView.as_view(), name='contract-bill'),
    path('contracts/<int:pk>/cancel/', views.cancel_contract, name='cancel-contract'),


    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-counties/', views.load_counties, name='ajax_load_counties'),
    path('ajax/load-positions/', views.load_positions, name='ajax_load_positions'),

    path('ajax/load-cities-supplier/', views.load_cities_supplier, name='ajax_load_cities_supplier'),
    path('ajax/load-counties-supplier/', views.load_counties_supplier, name='ajax_load_counties_supplier'),
    path('ajax/load-positions-supplier/', views.load_positions_supplier, name='ajax_load_positions_supplier'),
    path('buyer-info/<int:pk>/', views.get_buyer_info, name='buyer-info'),

]