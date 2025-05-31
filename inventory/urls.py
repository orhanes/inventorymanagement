from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('', views.StockListView.as_view(), name='inventory'),
    path('new/', views.StockCreateView.as_view(), name='new-stock'),
    path('stock/<int:pk>/edit/', views.StockUpdateView.as_view(), name='edit-stock'),
    path('stock/<int:pk>/delete/', views.StockDeleteView.as_view(), name='delete-stock'),
    path('stock/<int:pk>/view/', views.StockDetailView.as_view(), name='view-stock'),
    path('stockcard/<int:pk>/print/', views.print_stockcard, name='print-stockcard'),
    path('stock/<int:stock_id>/add_card/', views.add_stockcard, name='add-stockcard'),
    path('stockcard/<int:pk>/edit/', views.StockCardUpdateView.as_view(), name='edit-stockcard'),
    path('stockcard/<int:pk>/delete/', views.StockCardDeleteView.as_view(), name='delete-stockcard'),
    path('barcode-search/', views.barcode_search, name='barcode-search'),
    path('api/stockcard/lookup/', views.StockCardLookupAPI.as_view(), name='stockcard-lookup-api'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
]

router = DefaultRouter()
router.register(r'api/stockcard', views.StockCardViewSet, basename='api-stockcard')

urlpatterns += router.urls