import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction as db_transaction
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal

from .models import Vehicle, VehicleSharePurchase, VehiclePurchase
from .forms import SharePurchaseForm, VehiclePurchaseForm
from wallet.models import Wallet, Transaction

@login_required
def vehicle_list(request):
    """Display all available vehicles"""
    vehicles = Vehicle.objects.filter(status='available').order_by('-created_at')
    
    # Simple search
    search_query = request.GET.get('search', '')
    if search_query:
        vehicles = vehicles.filter(
            models.Q(name__icontains=search_query) |
            models.Q(model__icontains=search_query)
        )
    
    context = {
        'vehicles': vehicles,
        'search_query': search_query,
    }
    return render(request, 'vehicles/listing.html', context)

@login_required
def vehicle_detail(request, pk):
    """Display vehicle details"""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    share_form = SharePurchaseForm(vehicle=vehicle)
    purchase_form = VehiclePurchaseForm()
    
    # Get user's shares in this vehicle
    user_shares = VehicleSharePurchase.objects.filter(
        user=request.user, 
        vehicle=vehicle
    ).aggregate(total=models.Sum('shares_purchased'))['total'] or 0
    
    context = {
        'vehicle': vehicle,
        'share_form': share_form,
        'purchase_form': purchase_form,
        'user_shares': user_shares,
        'wallet_balance': request.user.wallet.balance,
    }
    return render(request, 'vehicles/detail.html', context)

@login_required
def buy_vehicle_shares(request, pk):
    """Process share purchase with complete transaction tracking"""
    vehicle = get_object_or_404(Vehicle, pk=pk, status='available')
    
    if request.method == 'POST':
        form = SharePurchaseForm(request.POST, vehicle=vehicle)
        
        if form.is_valid():
            shares = form.cleaned_data['shares']
            total_cost = shares * vehicle.share_price
            
            wallet = request.user.wallet
            
            # Check balance
            if wallet.balance < total_cost:
                messages.error(
                    request,
                    f'Insufficient balance. Need ${total_cost:,.2f}. Your balance: ${wallet.balance:,.2f}'
                )
                # Store purchase attempt in session
                request.session['pending_vehicle_share'] = {
                    'vehicle_id': vehicle.id,
                    'shares': shares,
                    'amount': str(total_cost)
                }
                return redirect('deposit')
            
            # Process purchase with database transaction
            with db_transaction.atomic():
                # Deduct from wallet
                wallet.balance -= total_cost
                wallet.save()
                
                # Update vehicle shares
                vehicle.available_shares -= shares
                vehicle.save()
                
                # Generate transaction reference
                transaction_ref = f"VS-{uuid.uuid4().hex[:12].upper()}"
                
                # Record share purchase in vehicles app
                share_purchase = VehicleSharePurchase.objects.create(
                    user=request.user,
                    vehicle=vehicle,
                    shares_purchased=shares,
                    price_per_share=vehicle.share_price,
                    total_amount=total_cost,
                    transaction_reference=transaction_ref
                )
                
                # Create wallet transaction record
                wallet_transaction = Transaction.objects.create(
                    user=request.user,
                    transaction_type='buy_vehicle_share',
                    amount=total_cost,
                    status='completed',  # Auto-complete for share purchases
                    description=f"Purchased {shares} shares of {vehicle.name} at ${vehicle.share_price}/share. Vehicle ID: {vehicle.id}",
                    reference_id=transaction_ref
                )
            
            messages.success(
                request,
                f'✅ Successfully purchased {shares} shares of {vehicle.name}!\n'
                f'Amount: ${total_cost:,.2f}\n'
                f'Transaction ID: {transaction_ref}'
            )
            return redirect('vehicle_detail', pk=vehicle.id)
        else:
            for error in form.errors.values():
                messages.error(request, error)
    
    return redirect('vehicle_detail', pk=vehicle.id)

@login_required
def buy_vehicle_full(request, pk):
    """Process full vehicle purchase with complete transaction tracking"""
    vehicle = get_object_or_404(Vehicle, pk=pk, status='available')
    
    if request.method == 'POST':
        form = VehiclePurchaseForm(request.POST)
        
        if form.is_valid():
            total_cost = vehicle.price
            wallet = request.user.wallet
            
            # Check balance
            if wallet.balance < total_cost:
                messages.error(
                    request,
                    f'Insufficient balance. Need ${total_cost:,.2f}. Your balance: ${wallet.balance:,.2f}'
                )
                request.session['pending_vehicle_purchase'] = {
                    'vehicle_id': vehicle.id,
                    'amount': str(total_cost)
                }
                return redirect('deposit')
            
            # Process purchase with database transaction
            with db_transaction.atomic():
                # Deduct from wallet
                wallet.balance -= total_cost
                wallet.save()
                
                # Mark vehicle as sold
                vehicle.status = 'sold'
                vehicle.save()
                
                # Generate transaction reference
                transaction_ref = f"VP-{uuid.uuid4().hex[:12].upper()}"
                
                # Record vehicle purchase
                vehicle_purchase = form.save(commit=False)
                vehicle_purchase.user = request.user
                vehicle_purchase.vehicle = vehicle
                vehicle_purchase.purchase_price = total_cost
                vehicle_purchase.transaction_reference = transaction_ref
                vehicle_purchase.save()
                
                # Create wallet transaction record
                wallet_transaction = Transaction.objects.create(
                    user=request.user,
                    transaction_type='buy_vehicle',
                    amount=total_cost,
                    status='completed',  # Auto-complete for vehicle purchases
                    description=f"Purchased {vehicle.name} (full vehicle). Vehicle ID: {vehicle.id}. Delivery address: {vehicle_purchase.delivery_address}",
                    reference_id=transaction_ref
                )
            
            messages.success(
                request,
                f'🎉 Congratulations! You have successfully purchased {vehicle.name}!\n'
                f'Amount: ${total_cost:,.2f}\n'
                f'Transaction ID: {transaction_ref}\n\n'
                f'We will contact you within 24 hours to arrange delivery.'
            )
            return redirect('my_purchases')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    
    return redirect('vehicle_detail', pk=vehicle.id)

@login_required
def my_shares(request):
    """Display user's vehicle shares"""
    shares = VehicleSharePurchase.objects.filter(
        user=request.user
    ).select_related('vehicle').order_by('-created_at')
    
    total_invested = sum(share.total_amount for share in shares)
    
    context = {
        'shares': shares,
        'total_invested': total_invested,
    }
    return render(request, 'vehicles/my_shares.html', context)

@login_required
def my_purchases(request):
    """Display user's vehicle purchases"""
    purchases = VehiclePurchase.objects.filter(
        user=request.user
    ).select_related('vehicle').order_by('-created_at')
    
    context = {
        'purchases': purchases,
    }
    return render(request, 'vehicles/my_purchases.html', context)

@login_required
def vehicle_transaction_history(request, vehicle_id=None):
    """View transaction history for vehicles"""
    transactions = Transaction.objects.filter(
        user=request.user,
        transaction_type__in=['buy_vehicle_share', 'buy_vehicle']
    ).order_by('-created_at')
    
    if vehicle_id:
        transactions = transactions.filter(description__icontains=f"Vehicle ID: {vehicle_id}")
    
    context = {
        'transactions': transactions,
    }
    return render(request, 'vehicles/transaction_history.html', context)