from django import forms
from .models import Account, Card


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('account_type', 'currency')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.balance = 0



class TransferForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['from_account'].queryset = Account.objects.filter(owner=user)

    from_account = forms.ModelChoiceField(queryset=Account.objects.none())
    to_account = forms.ModelChoiceField(queryset=Account.objects.all())
    amount = forms.DecimalField(min_value=0.01)
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}))


class CardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['account'].queryset = Account.objects.filter(owner=user)

    class Meta:
        model = Card
        fields = ('account', 'card_type', 'expiry_date')
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }