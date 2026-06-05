# portfolio/context_processors.py

from .utils import get_user_total_shares, evaluate_share_tiers

def share_status(request):
    if request.user.is_authenticated:
        total = get_user_total_shares(request.user)
        achieved, next_target = evaluate_share_tiers(total)

        return {
            "total_shares": total,
            "achieved_tiers": achieved,
            "next_tier": next_target,
        }

    return {}