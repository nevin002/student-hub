from django import forms
from django.contrib.auth.models import User
from .models import Expense


class ExpenseForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text='Select all participants (including yourself)'
    )
    
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'participants']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
        }
