from django.contrib import admin
from django.utils import timezone
from .models import Wallet, Transaction

@admin.action(description='Mark selected transactions as completed')
def make_completed(modeladmin, request, queryset):
    for transaction in queryset:
        if transaction.status != 'completed' and transaction.transaction_type in ['deposit', 'withdrawal']:
            transaction.status = 'completed'
            transaction.completed_at = timezone.now()
            transaction.save()
            # Update wallet balance for deposits and withdrawals
            if transaction.transaction_type == 'deposit':
                wallet = transaction.user.wallet
                wallet.balance += transaction.amount
                wallet.save()
            elif transaction.transaction_type == 'withdrawal':
                wallet = transaction.user.wallet
                wallet.balance -= transaction.amount
                wallet.save()
    modeladmin.message_user(request, f"{queryset.count()} transactions marked as completed.")

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('reference_id', 'user', 'transaction_type', 'amount', 'status', 'created_at')
    list_filter = ('status', 'transaction_type')
    actions = [make_completed]
    readonly_fields = ('reference_id', 'created_at')

admin.site.register(Wallet)
admin.site.register(Transaction, TransactionAdmin)