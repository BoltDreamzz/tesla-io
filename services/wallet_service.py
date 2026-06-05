# services/wallet_service.py

from django.db import transaction
from decimal import Decimal

from wallet.models import Wallet, Transaction


class WalletService:

    @staticmethod
    @transaction.atomic
    def update_wallet(
        *,
        user,
        amount,
        direction,
        transaction_type,
        performed_by,
        description=""
    ):

        wallet = Wallet.objects.select_for_update().get(
            user=user
        )

        balance_before = wallet.balance

        # if direction == "credit":

        wallet.balance += amount

        # elif direction == "debit":

            # if wallet.balance < amount:
            #     raise ValueError(
            #         "Insufficient balance."
            #     )

            # wallet.balance -= amount

        balance_after = wallet.balance

        wallet.save()

        txn = Transaction.objects.create(
            user=user,
            amount=amount,
            # direction=direction,
            transaction_type=transaction_type,
            balance_before=balance_before,
            balance_after=balance_after,
            performed_by=performed_by,
            description=description,
            status="completed"
        )

        return txn