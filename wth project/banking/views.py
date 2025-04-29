from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.


from django.views.generic import ListView, DetailView, CreateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Account, Transaction, Card
from .forms import AccountForm, TransferForm, CardForm


class AccountListView(ListView):
    model = Account
    template_name = 'banking/account_list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class AccountDetailView(DetailView):
    model = Account
    template_name = 'banking/account_detail.html'
    context_object_name = 'account'

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'banking/account_create.html'
    success_url = reverse_lazy('account-list')

    def form_valid(self, form):
        account = form.save(commit=False)
        account.owner = self.request.user
        account.number = f"AC{self.request.user.id}{Account.objects.count() + 1}"
        account.balance = 0
        account.save()
        messages.success(self.request, "Account created successfully!")
        return super().form_valid(form)

class AccountDeleteView(DeleteView):
    model = Account
    template_name = 'banking/account_confirm_delete.html'
    success_url = reverse_lazy('account-list')

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user, balance=0)

    def delete(self, request, *args, **kwargs):
        account = self.get_object()
        if account.balance > 0:
            messages.error(request, "Cannot delete account with balance")
            return redirect('account-detail', pk=account.pk)
        messages.success(request, "Account deleted successfully!")
        return super().delete(request, *args, **kwargs)


class TransactionListView(ListView):
    model = Transaction
    template_name = 'banking/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 10

    def get_queryset(self):
        user_accounts = Account.objects.filter(owner=self.request.user)
        return Transaction.objects.filter(
            Q(from_account__in=user_accounts) |
            Q(to_account__in=user_accounts)
        ).order_by('-date')


class TransferView(FormView):
    form_class = TransferForm
    template_name = 'banking/transfer.html'
    success_url = reverse_lazy('transaction-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        from_account = form.cleaned_data['from_account']
        to_account = form.cleaned_data['to_account']
        amount = form.cleaned_data['amount']
        description = form.cleaned_data.get('description', '')

        from_account.balance -= amount
        to_account.balance += amount

        from_account.save()
        to_account.save()

        Transaction.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount,
            description=description
        )

        messages.success(self.request, "Transfer completed successfully!")
        return super().form_valid(form)


class CardListView(ListView):
    model = Card
    template_name = 'banking/card_list.html'
    context_object_name = 'cards'

    def get_queryset(self):
        return Card.objects.filter(account__owner=self.request.user)


class CardCreateView(CreateView):
    model = Card
    form_class = CardForm
    template_name = 'banking/card_create.html'
    success_url = reverse_lazy('card-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        card = form.save(commit=False)
        account = form.cleaned_data['account']
        card.number = f"4{self.request.user.id:04d}{account.id:04d}{Card.objects.count() + 1:04d}"
        card.owner_name = f"{self.request.user.first_name} {self.request.user.last_name}"
        card.save()
        messages.success(self.request, "Card created successfully!")
        return super().form_valid(form)