from .models import Transaction

def pending_deposits_count(request):
    if request.user.is_authenticated and request.user.is_staff:
        count = Transaction.objects.filter(
            transaction_type='deposit',
            status='pending'
        ).count()
        return {'pending_deposits_count': count}

    return {'pending_deposits_count': 0}