from django.urls import path
from .views import (
    AccountListView, AccountDetailView, AccountCreateView, AccountDeleteView,
    TransactionListView, TransferView, CardListView, CardCreateView
)

urlpatterns = [
    path('accounts/', AccountListView.as_view(), name='account-list'),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('accounts/open/', AccountCreateView.as_view(), name='account-create'),
    path('accounts/<int:pk>/close/', AccountDeleteView.as_view(), name='account-delete'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('cards/', CardListView.as_view(), name='card-list'),
    path('cards/new/', CardCreateView.as_view(), name='card-create'),
]