from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from vehicles.models import Vehicle

def landing(request):
    vehicles = Vehicle.objects.all().order_by("-name")
    return render(request, 'core/tesla.html', {
        'vehicles': vehicles,
    })

@login_required
def dashboard(request):
    user = request.user
    wallet = user.wallet
    holdings = user.holding_set.all()
    recent_transactions = user.transactions.all().order_by('-created_at')[:5]
    context = {
        'wallet': wallet,
        'holdings': holdings,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'core/dashboard.html', context)