from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Wallet, Transaction
from .forms import DepositForm, WithdrawForm, PaymentConfirmationForm

from django.core.mail import send_mail
from django.conf import settings
import qrcode
import io
import base64
    
@login_required
def payment_instructions(request, transaction_id):
    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user
    )

    if transaction.status != 'payment_pending':
        messages.error(request, 'This transaction is no longer pending payment.')
        return redirect('deposit')

    payment_info = settings.PAYMENT_METHODS.get(
        transaction.payment_method, {}
    )

    qr_code_base64 = None
    if payment_info.get('type') == 'crypto' and payment_info.get('address'):
        qr_code_base64 = generate_qr_code(
            payment_info['address'],
            transaction.amount
        )

    # ✅ Generate reference ONCE and store it
    if not transaction.payment_reference:
        transaction.payment_reference = generate_payment_reference(transaction)
        transaction.save()

    if request.method == "POST":
        form = PaymentConfirmationForm(request.POST, request.FILES)

        if form.is_valid():
            transaction.proof_of_payment = form.cleaned_data['proof_of_payment']
            transaction.status = "pending_confirmation"
            transaction.save()

            messages.success(
                request,
                "Payment proof uploaded successfully. Awaiting confirmation."
            )
            return redirect("dashboard")
    else:
        form = PaymentConfirmationForm()

    return render(
        request,
        'wallet/payment_instructions.html',
        {
            'transaction': transaction,
            'payment_info': payment_info,
            'form': form,
            'qr_code_base64': qr_code_base64,
        }
    )


def generate_payment_reference(transaction): 
    """ Generate a unique payment reference that matches the expected format for the payment method """ # Format based on payment method
    if transaction.payment_method == 'bank_transfer': 
        # Format: DEPOSIT-{USER_ID}-{TRANSACTION_ID}-{TIMESTAMP} 
        return f"DEP-{transaction.user.id:06d}-{transaction.id:08d}" 
    elif transaction.payment_method in ['usdt', 'usdc', 'ethereum']: 
        # Format for crypto: {TXID}-{TIMESTAMP} but we'll create a placeholder # User will actually use their transaction hash, but we prepopulate with format 
        timestamp = transaction.created_at.strftime('%Y%m%d%H%M%S')
        return f"TX-{transaction.reference_id[-8:]}-{timestamp}" 
    elif transaction.payment_method == 'btc': 
        # Format for Bitcoin 
        return f"BTC-{transaction.reference_id[-10:]}" 
    else: # Default format 
        return transaction.reference_id


def generate_qr_code(data, amount=None):
    """Generate QR code for crypto address"""
  
    # Format data for different cryptocurrencies
    if amount:
        if data.startswith('bc1') or data.startswith('1') or data.startswith('3'):
            data = f"bitcoin:{data}?amount={amount}"
        elif data.startswith('0x'):
            data = f"ethereum:{data}?value={amount}"
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding in HTML
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    # Encode to base64
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_base64}"

def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_method = form.cleaned_data['payment_method']
            
            transaction = Transaction.objects.create(
                user=request.user,
                transaction_type='deposit',
                amount=amount,
                status='payment_pending',  # New status
                payment_method=payment_method,
                description=f"Deposit request for ${amount} via {payment_method}"
            )
            
            # Store transaction ID in session for redirect after payment
            request.session['pending_transaction_id'] = transaction.id
            
            # Redirect to payment instructions page
            return redirect('payment_instructions', transaction_id=transaction.id)
    else:
        form = DepositForm()
    
    return render(request, 'wallet/deposit.html', {
        'form': form, 
        'wallet': request.user.wallet,
        'payment_methods': settings.PAYMENT_METHODS
    })

# @login_required
# def payment_instructions(request, transaction_id):
#     transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
#     # Ensure transaction is in payment_pending state
#     if transaction.status != 'payment_pending':
#         messages.error(request, 'This transaction is no longer pending payment.')
#         return redirect('deposit')
    
#     payment_info = settings.PAYMENT_METHODS.get(transaction.payment_method, {})
    
#     if request.method == 'POST':
#         form = PaymentConfirmationForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Update transaction with payment proof
#             transaction.proof_of_payment = form.cleaned_data['proof_of_payment']
#             transaction.payment_reference = form.cleaned_data['payment_reference']
#             transaction.status = 'pending'
#             transaction.save()
            
#             # Notify admin
#             notify_admin_of_payment(transaction)
            
#             messages.success(request, 'Payment confirmation submitted. Your deposit will be processed shortly.')
#             return redirect('payment_pending', transaction_id=transaction.id)
#     else:
#         form = PaymentConfirmationForm()
    
#     return render(request, 'wallet/payment_instructions.html', {
#         'transaction': transaction,
#         'payment_info': payment_info,
#         'form': form
#     })

@login_required
def payment_instructions(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    # Ensure transaction is in payment_pending state
    if transaction.status != 'payment_pending':
        messages.error(request, 'This transaction is no longer pending payment.')
        return redirect('deposit')
    
    payment_info = settings.PAYMENT_METHODS.get(transaction.payment_method, {})
    
    # Generate QR code for crypto payments
    qr_code_base64 = None
    if payment_info.get('type') == 'crypto' and payment_info.get('address'):
        qr_code_base64 = generate_qr_code(payment_info['address'], transaction.amount)
    
    if request.method == 'POST':
        form = PaymentConfirmationForm(request.POST, request.FILES)
        if form.is_valid():
            # Update transaction with payment proof
            # if 'proof_of_payment' in request.FILES:
            transaction.proof_of_payment = request.FILES['proof_of_payment']
            # transaction.payment_reference = form.cleaned_data['payment_reference']
            transaction.status = 'pending'
            transaction.save()
            
            # Notify admin
            notify_admin_of_payment(transaction)
            
            messages.success(request, 'Payment confirmation submitted. Your deposit will be processed shortly.')
            return redirect('payment_pending', transaction_id=transaction.id)
    else:
        form = PaymentConfirmationForm()
    
    return render(request, 'wallet/payment_instructions.html', {
        'transaction': transaction,
        'payment_info': payment_info,
        'form': form,
        'qr_code_base64': qr_code_base64,
    })

def generate_qr_code(data, amount=None):
    """
    Generate QR code for crypto address with optional amount
    Returns base64 encoded image string
    """
    # Format data for different cryptocurrencies
    if amount:
        # For Bitcoin with amount
        if data.startswith('bc1') or data.startswith('1') or data.startswith('3'):
            data = f"bitcoin:{data}?amount={amount}"
        # For Ethereum/USDT/USDC with amount
        elif data.startswith('0x'):
            data = f"ethereum:{data}?value={amount}"
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding in HTML
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    # Encode to base64
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_base64}"

@login_required
def payment_pending(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    if transaction.status == 'completed':
        messages.success(request, 'Your deposit has been completed!')
        return redirect('wallet_dashboard')
    elif transaction.status == 'failed':
        messages.error(request, 'Your deposit was declined. Please contact support if you believe this is an error.')
        return redirect('deposit')
    
    return render(request, 'wallet/payment_pending.html', {
        'transaction': transaction
    })

@login_required
@user_passes_test(is_admin)
def admin_transactions(request):
    pending_transactions = Transaction.objects.filter(
        transaction_type='deposit',
        status='pending'
    ).order_by('-created_at')
    
    return render(request, 'admin/transactions.html', {
        'pending_transactions': pending_transactions
    })

@login_required
@user_passes_test(is_admin)
def admin_process_transaction(request, transaction_id, action):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    if transaction.status != 'pending':
        messages.error(request, 'This transaction has already been processed.')
        return redirect('admin_transactions')
    
    if action == 'approve':
        # Add money to wallet
        wallet = transaction.user.wallet
        wallet.balance += transaction.amount
        wallet.save()
        
        # Update transaction status
        transaction.status = 'completed'
        transaction.save()
        
        # Notify user
        notify_user_of_approval(transaction)
        
        messages.success(request, f'Approved deposit of ${transaction.amount} for {transaction.user.username}')
        
    elif action == 'decline':
        transaction.status = 'failed'
        transaction.save()
        
        # Notify user
        notify_user_of_decline(transaction)
        
        messages.success(request, f'Declined deposit of ${transaction.amount} for {transaction.user.username}')
    
    return redirect('admin_transactions')

def notify_admin_of_payment(transaction):
    """Send email notification to admin about new payment submission"""
    subject = f'New Deposit Payment Submitted - {transaction.reference_id}'
    message = f"""
    A user has submitted payment confirmation:
    
    User: {transaction.user.username} ({transaction.user.email})
    Amount: ${transaction.amount}
    Payment Method: {transaction.payment_method}
    Reference: {transaction.payment_reference}
    Transaction ID: {transaction.reference_id}
    
    Please review and approve/decline at: {settings.SITE_URL}/admin/transactions/
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        fail_silently=False,
    )

def notify_user_of_approval(transaction):
    """Send email notification to user about approved deposit"""
    subject = f'Deposit Approved - {transaction.reference_id}'
    message = f"""
    Your deposit of ${transaction.amount} has been approved and added to your wallet.
    
    Transaction ID: {transaction.reference_id}
    New Balance: ${transaction.user.wallet.balance}
    
    Thank you for investing with Teslainvest!
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [transaction.user.email],
        fail_silently=False,
    )

def notify_user_of_decline(transaction):
    """Send email notification to user about declined deposit"""
    subject = f'Deposit Declined - {transaction.reference_id}'
    message = f"""
    Your deposit request of ${transaction.amount} has been declined.
    
    Transaction ID: {transaction.reference_id}
    
    If you believe this is an error, please contact support with your transaction details.
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [transaction.user.email],
        fail_silently=False,
    )


@login_required
def withdraw(request):
    wallet = request.user.wallet
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_method = form.cleaned_data['payment_method']
            if payment_method != 'bank_transfer':
                if amount > wallet.balance:
                    messages.error(request, 'Insufficient balance.')
                    return redirect('withdraw')
                bank_details = form.cleaned_data['bank_details']
                transaction = Transaction.objects.create(
                    user=request.user,
                    transaction_type='withdrawal',
                    amount=amount,
                    status='pending',
                    description=f"Withdrawal request to {bank_details}"
                )
                messages.success(request, f'Withdrawal request for ${amount} submitted. Reference ID: {transaction.reference_id}')
                return redirect('transaction_list')
            else:
                messages.error(request, 'Bank transfers are currently unavailable. Select another payment method.')
                return redirect('withdraw')
    else:
        form = WithdrawForm()
    return render(request, 'wallet/withdraw.html', {'form': form, 'wallet': wallet})

@login_required
def transaction_list(request):
    user = request.user

    # transactions = request.user.transactions.all().order_by('-created_at')
    # recent_transactions = user.transactions.all().order_by('-created_at')[:5]
    recent_transactions = user.transactions.filter(status__in=['completed', 'failed', 'cancelled']).order_by('-created_at')[:15]
    return render(request, 'wallet/transaction_list.html', {'recent_transactions': recent_transactions})