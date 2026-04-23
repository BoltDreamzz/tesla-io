from django.urls import path
from . import views

urlpatterns = [
    path('buy/', views.buy_stock, name='buy_stock'),
    path('portfolio/', views.portfolio, name='portfolio'),
]