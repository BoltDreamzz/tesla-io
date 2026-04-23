from django.urls import path
from . import views
    
urlpatterns = [
path('deposit/', views.deposit, name='deposit'),
    path('payment-instructions/<int:transaction_id>/', views.payment_instructions, name='payment_instructions'),
    path('payment-pending/<int:transaction_id>/', views.payment_pending, name='payment_pending'),
    path('admin/transactions/', views.admin_transactions, name='admin_transactions'),
    path('admin/process/<int:transaction_id>/<str:action>/', views.admin_process_transaction, name='admin_process_transaction'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transactions/', views.transaction_list, name='transaction_list'),
]