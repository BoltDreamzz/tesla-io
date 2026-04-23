from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),
    path('<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('<int:pk>/buy-shares/', views.buy_vehicle_shares, name='buy_shares'),
    path('<int:pk>/buy-vehicle/', views.buy_vehicle_full, name='buy_vehicle'),
    path('my-shares/', views.my_shares, name='my_shares'),
    path('my-purchases/', views.my_purchases, name='my_purchases'),
    path('transactions/', views.vehicle_transaction_history, name='transaction_history'),  # New
    path('transactions/<int:vehicle_id>/', views.vehicle_transaction_history, name='vehicle_transactions'),  # New
]