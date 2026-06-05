# portfolio/utils.py

from django.db.models import Sum
from .models import Holding

def get_user_total_shares(user):
    total = (
        Holding.objects
        .filter(user=user)
        .aggregate(total=Sum("quantity"))["total"]
    )
    return total or 0


# portfolio/utils.py

from .tiers import SHARE_TIERS

def evaluate_share_tiers(total_shares):
    achieved = []
    next_target = None

    for tier in SHARE_TIERS:
        if total_shares >= tier["required"]:
            achieved.append(tier)
        elif not next_target:
            next_target = {
                **tier,
                "remaining": tier["required"] - total_shares
            }

    return achieved, next_target