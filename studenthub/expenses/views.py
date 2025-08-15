from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from .models import Expense
from .forms import ExpenseForm


@login_required
def expense_list(request):
    # Get all expenses where current user is a participant
    user_expenses = Expense.objects.filter(participants=request.user).order_by('-created_at')
    
    # Calculate net balance
    total_paid = Expense.objects.filter(payer=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    total_owes = 0
    for expense in Expense.objects.filter(participants=request.user).exclude(payer=request.user):
        total_owes += expense.per_head()
    
    net_balance = total_paid - total_owes
    
    context = {
        'expenses': user_expenses,
        'total_paid': total_paid,
        'total_owes': total_owes,
        'net_balance': net_balance,
    }
    return render(request, 'expenses/expense_list.html', context)


@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.payer = request.user
            expense.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Expense created successfully!')
            return redirect('expenses:expense_list')
    else:
        form = ExpenseForm()
        # Pre-select current user in participants
        form.fields['participants'].initial = [request.user]
    
    context = {
        'form': form,
        'title': 'Create New Expense',
    }
    return render(request, 'expenses/expense_form.html', context)
