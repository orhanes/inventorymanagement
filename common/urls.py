from django.urls import path
from django.urls import re_path as url
from . import views

urlpatterns = [
    # Firma URL'leri
    path('company-settings/', views.company_settings, name='company_settings'),
    
    # Kategori URL'leri
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Alt Kategori URL'leri
    path('subcategories/', views.subcategory_list, name='subcategory_list'),
    path('subcategories/create/', views.subcategory_create, name='subcategory_create'),
    path('subcategories/<int:pk>/edit/', views.subcategory_edit, name='subcategory_edit'),
    path('subcategories/<int:pk>/delete/', views.subcategory_delete, name='subcategory_delete'),
    
    # Birim URL'leri
    path('units/', views.unit_list, name='unit_list'),
    path('units/create/', views.unit_create, name='unit_create'),
    path('units/<int:pk>/edit/', views.unit_edit, name='unit_edit'),
    path('units/<int:pk>/delete/', views.unit_delete, name='unit_delete'),
    
    path('tax-rates/', views.tax_rate_list, name='tax_rate_list'),
    path('tax-rates/create/', views.tax_rate_create, name='tax_rate_create'),
    path('tax-rates/<int:pk>/edit/', views.tax_rate_edit, name='tax_rate_edit'),
    path('tax-rates/<int:pk>/delete/', views.tax_rate_delete, name='tax_rate_delete'),
    
    path('address-types/', views.address_type_list, name='address_type_list'),
    path('address-types/create/', views.address_type_create, name='address_type_create'),
    path('address-types/<int:pk>/edit/', views.address_type_edit, name='address_type_edit'),
    path('address-types/<int:pk>/delete/', views.address_type_delete, name='address_type_delete'),
    
    # Departman URL'leri
    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_edit, name='department_edit'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),
    
    # Pozisyon URL'leri
    path('positions/', views.position_list, name='position_list'),
    path('positions/create/', views.position_create, name='position_create'),
    path('positions/<int:pk>/edit/', views.position_edit, name='position_edit'),
    path('positions/<int:pk>/delete/', views.position_delete, name='position_delete'),
    
    # Banka Türü URL'leri
    path('bank-types/', views.bank_type_list, name='bank_type_list'),
    path('bank-types/create/', views.bank_type_create, name='bank_type_create'),
    path('bank-types/<int:pk>/edit/', views.bank_type_edit, name='bank_type_edit'),
    path('bank-types/<int:pk>/delete/', views.bank_type_delete, name='bank_type_delete'),
    
    # Banka URL'leri
    path('banks/', views.bank_list, name='bank_list'),
    path('banks/create/', views.bank_create, name='bank_create'),
    path('banks/<int:pk>/edit/', views.bank_edit, name='bank_edit'),
    path('banks/<int:pk>/delete/', views.bank_delete, name='bank_delete'),
    
    # Para Birimi URL'leri
    path('currencies/', views.currency_list, name='currency_list'),
    path('currencies/create/', views.currency_create, name='currency_create'),
    path('currencies/<int:pk>/edit/', views.currency_edit, name='currency_edit'),
    path('currencies/<int:pk>/delete/', views.currency_delete, name='currency_delete'),
    
    # Ödeme Türü URL'leri
    path('payment-types/', views.payment_type_list, name='payment_type_list'),
    path('payment-types/create/', views.payment_type_create, name='payment_type_create'),
    path('payment-types/<int:pk>/edit/', views.payment_type_edit, name='payment_type_edit'),
    path('payment-types/<int:pk>/delete/', views.payment_type_delete, name='payment_type_delete'),
    
    # Ödeme Yöntemi URL'leri
    path('payment-methods/', views.payment_method_list, name='payment_method_list'),
    path('payment-methods/create/', views.payment_method_create, name='payment_method_create'),
    path('payment-methods/<int:pk>/edit/', views.payment_method_edit, name='payment_method_edit'),
    path('payment-methods/<int:pk>/delete/', views.payment_method_delete, name='payment_method_delete'),
    
    # Nakliye Türü URL'leri
    path('delivery-types/', views.delivery_type_list, name='delivery_type_list'),
    path('delivery-types/create/', views.delivery_type_create, name='delivery_type_create'),
    path('delivery-types/<int:pk>/edit/', views.delivery_type_edit, name='delivery_type_edit'),
    path('delivery-types/<int:pk>/delete/', views.delivery_type_delete, name='delivery_type_delete'),
    
    # Nakliye Firması URL'leri
    path('delivery-companies/', views.delivery_company_list, name='delivery_company_list'),
    path('delivery-companies/create/', views.delivery_company_create, name='delivery_company_create'),
    path('delivery-companies/<int:pk>/edit/', views.delivery_company_edit, name='delivery_company_edit'),
    path('delivery-companies/<int:pk>/delete/', views.delivery_company_delete, name='delivery_company_delete'),
    
    # Araç Tipi URL'leri
    path('vehicle-types/', views.vehicle_type_list, name='vehicle_type_list'),
    path('vehicle-types/create/', views.vehicle_type_create, name='vehicle_type_create'),
    path('vehicle-types/<int:pk>/edit/', views.vehicle_type_edit, name='vehicle_type_edit'),
    path('vehicle-types/<int:pk>/delete/', views.vehicle_type_delete, name='vehicle_type_delete'),
    
    # Araç Markası URL'leri
    path('vehicle-brands/', views.vehicle_brand_list, name='vehicle_brand_list'),
    path('vehicle-brands/create/', views.vehicle_brand_create, name='vehicle_brand_create'),
    path('vehicle-brands/<int:pk>/edit/', views.vehicle_brand_edit, name='vehicle_brand_edit'),
    path('vehicle-brands/<int:pk>/delete/', views.vehicle_brand_delete, name='vehicle_brand_delete'),
    
    # Araç Modeli URL'leri
    path('vehicle-models/', views.vehicle_model_list, name='vehicle_model_list'),
    path('vehicle-models/create/', views.vehicle_model_create, name='vehicle_model_create'),
    path('vehicle-models/<int:pk>/edit/', views.vehicle_model_edit, name='vehicle_model_edit'),
    path('vehicle-models/<int:pk>/delete/', views.vehicle_model_delete, name='vehicle_model_delete'),
]

