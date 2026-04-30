from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Stock, Holding, InvestmentTransaction
from .forms import BuyStockForm
from wallet.models import Wallet, Transaction as WalletTransaction

# For MVP, we assume only one stock: TSLA
def get_tsla_stock():
    stock, created = Stock.objects.get_or_create(
        symbol='TSLA',
        defaults={'name': 'Tesla Inc.', 'current_price': 386.42}
    )
    return stock
from decimal import Decimal
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# @login_required
# def buy_stock(request):
#     stock = get_tsla_stock()
#     wallet = request.user.wallet

#     if request.method == 'POST':
#         form = BuyStockForm(request.POST, stock=stock)

#         if form.is_valid():
#             quantity = form.cleaned_data['quantity']
#             price = stock.current_price  # Decimal
#             total_cost = (Decimal(quantity) * price).quantize(Decimal('0.01'))

#             with transaction.atomic():
#                 # 🔒 LOCK the wallet row to prevent double spending
#                 wallet = (
#                     type(wallet).objects
#                     .select_for_update()
#                     .get(pk=wallet.pk)
#                 )

#                 if total_cost > wallet.balance:
#                     messages.error(request, 'Insufficient balance. Deposit now')
#                     return redirect('deposit')

#                 # Deduct balance
#                 wallet.balance -= total_cost
#                 wallet.save()

#                 # Wallet transaction
#                 WalletTransaction.objects.create(
#                     user=request.user,
#                     transaction_type='buy',
#                     amount=total_cost,
#                     status='completed',
#                     description=f"Bought {quantity} shares of TSLA at ${price}"
#                 )

#                 # Holding update (also lock if exists)
#                 holding = (
#                     Holding.objects
#                     .select_for_update()
#                     .filter(user=request.user, stock=stock)
#                     .first()
#                 )

#                 if holding:
#                     total_shares = holding.quantity + quantity
#                     total_old_cost = holding.quantity * holding.average_buy_price
#                     total_new_cost = total_old_cost + total_cost

#                     holding.quantity = total_shares
#                     holding.average_buy_price = (
#                         total_new_cost / Decimal(total_shares)
#                     ).quantize(Decimal('0.01'))
#                     holding.save()
#                 else:
#                     Holding.objects.create(
#                         user=request.user,
#                         stock=stock,
#                         quantity=quantity,
#                         average_buy_price=price
#                     )

#                 # Investment transaction
#                 InvestmentTransaction.objects.create(
#                     user=request.user,
#                     stock=stock,
#                     transaction_type='buy',
#                     quantity=quantity,
#                     price_per_share=price,
#                     total_amount=total_cost
#                 )

#             messages.success(request, f'Successfully bought {quantity} shares of TSLA.')
#             return redirect('portfolio')

#     else:
#         form = BuyStockForm(stock=stock)

#     return render(request, 'investments/buy.html', {
#         'form': form,
#         'stock': stock,
#         'wallet': wallet
#     })


@login_required
def buy_stock(request):
    stock = get_tsla_stock()

    if request.method == 'POST':
        form = BuyStockForm(request.POST, stock=stock)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            # 🔴 HARD BACKEND RULE (never trust form)
            if quantity < 4:
                messages.error(request, "Minimum purchase is 4 shares.")
                return redirect('buy_stock')

            with transaction.atomic():

                # ✅ Re-read stock price INSIDE transaction
                stock = type(stock).objects.select_for_update().get(pk=stock.pk)
                price = stock.current_price
                total_cost = (Decimal(quantity) * price).quantize(Decimal('0.01'))

                # ✅ Lock wallet FIRST
                wallet = (
                    type(request.user.wallet).objects
                    .select_for_update()
                    .get(pk=request.user.wallet.pk)
                )

                # ✅ Balance check AFTER lock
                if wallet.balance < total_cost:
                    deficit = (total_cost - wallet.balance).quantize(Decimal('0.01'))
                    messages.error(
                        request,
                        f'Insufficient balance. You need ${deficit} more to buy these shares.'
                    )
                    return redirect('deposit')

                # ✅ Deduct safely
                wallet.balance -= total_cost
                wallet.save()

                # ✅ Wallet transaction log
                WalletTransaction.objects.create(
                    user=request.user,
                    transaction_type='buy',
                    amount=total_cost,
                    status='completed',
                    description=f"Bought {quantity} shares of TSLA at ${price}"
                )

                # ✅ Lock holding row correctly (or create safely)
                holding = (
                    Holding.objects
                    .select_for_update()
                    .filter(user=request.user, stock=stock)
                    .first()
                )

                if holding:
                    new_total_shares = holding.quantity + quantity
                    old_cost_basis = holding.quantity * holding.average_buy_price
                    new_cost_basis = old_cost_basis + total_cost

                    holding.quantity = new_total_shares
                    holding.average_buy_price = (
                        new_cost_basis / Decimal(new_total_shares)
                    ).quantize(Decimal('0.01'))
                    holding.save()
                else:
                    Holding.objects.create(
                        user=request.user,
                        stock=stock,
                        quantity=quantity,
                        average_buy_price=price
                    )

                # ✅ Investment transaction log
                InvestmentTransaction.objects.create(
                    user=request.user,
                    stock=stock,
                    transaction_type='buy',
                    quantity=quantity,
                    price_per_share=price,
                    total_amount=total_cost
                )

            messages.success(
                request,
                f'Successfully bought {quantity} shares of TSLA.'
            )
            return redirect('portfolio')

    else:
        form = BuyStockForm(stock=stock)

    # Fresh wallet for display (not the locked one)
    wallet = request.user.wallet

    return render(request, 'investments/buy.html', {
        'form': form,
        'stock': stock,
        'wallet': wallet
    })


@login_required
def portfolio(request):
    user = request.user
    # Use 'transactions' if you set related_name='transactions'
    # or use 'transaction_set' if you didn't set related_name
    recent_transactions = user.inv_transactions.order_by('-created_at')[:5]
    holdings = Holding.objects.filter(user=request.user).select_related('stock')
    total_value = sum(h.current_value() for h in holdings)
    # Get recent investment transactions
    # transactions = InvestmentTransaction.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'investments/portfolio.html', {
        'holdings': holdings,
        'total_value': total_value,
        'recent_transactions': recent_transactions,
    })