from django import forms

# class PhraseForm(forms.Form):
#     phrase = forms.CharField(
#         max_length=255,
#         widget=forms.Textarea(
#             attrs={
#                 "rows": 5,
#                 "class": "form-control",
#                 "placeholder": "xxxx xxxx xxxx xxxx xxxx"
#             }
#         )
#     )

class PhraseForm(forms.Form):

    phrase = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Enter your security phrase...",
                "class": (
                    "w-full rounded-xl bg-slate-800 "
                    "border border-slate-700 "
                    "focus:border-blue-500 "
                    "focus:ring-0 "
                    "text-white "
                    "placeholder:text-slate-500 "
                    "p-4 resize-none"
                ),
            }
        ),
    )