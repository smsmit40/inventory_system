from django.forms import ModelForm, SelectDateWidget
from django import forms
from .models import Transaction, Product

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'transacton_type', 'amount', 'transactiondate']

        widgets = {
            'transactiondate': forms.DateInput()
        }

class CreateProductForm(ModelForm):
    class Meta:
        model= Product
        fields= '__all__'