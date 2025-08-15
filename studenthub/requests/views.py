from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from .models import Request, RequestOffer, RequestFulfillment
from .forms import RequestForm, RequestOfferForm, RequestFilterForm


def request_list(request):
    """Display all requests with filtering and search"""
    requests_list = Request.objects.all().select_related('requester').prefetch_related('offers')
    
    # Apply filters
    form = RequestFilterForm(request.GET)
    if form.is_valid():
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')
        min_fee = form.cleaned_data.get('min_fee')
        max_fee = form.cleaned_data.get('max_fee')
        is_urgent = form.cleaned_data.get('is_urgent')
        search = form.cleaned_data.get('search')
        
        if category:
            requests_list = requests_list.filter(category=category)
        if status:
            requests_list = requests_list.filter(status=status)
        if min_fee is not None:
            requests_list = requests_list.filter(fee__gte=min_fee)
        if max_fee is not None:
            requests_list = requests_list.filter(fee__lte=max_fee)
        if is_urgent:
            requests_list = requests_list.filter(is_urgent=True)
        if search:
            requests_list = requests_list.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
    
    # Pagination
    paginator = Paginator(requests_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'total_requests': requests_list.count(),
        'open_requests': requests_list.filter(status='open').count(),
        'urgent_requests': requests_list.filter(is_urgent=True, status='open').count(),
    }
    
    return render(request, 'requests/request_list.html', context)


@login_required
def request_create(request):
    """Create a new request"""
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.requester = request.user
            request_obj.save()
            
            messages.success(request, 'Your request has been created successfully!')
            return redirect('requests:request_detail', pk=request_obj.pk)
    else:
        form = RequestForm()
    
    return render(request, 'requests/request_form.html', {'form': form, 'action': 'Create'})


def request_detail(request, pk):
    """Display request details and allow offers"""
    request_obj = get_object_or_404(Request, pk=pk)
    offers = request_obj.offers.all().select_related('fulfiller')
    
    # Check if user has already made an offer
    user_offer = None
    if request.user.is_authenticated:
        user_offer = offers.filter(fulfiller=request.user).first()
    
    # Form for making offers
    offer_form = None
    if request.user.is_authenticated and request_obj.can_be_fulfilled:
        if request.method == 'POST':
            offer_form = RequestOfferForm(request.POST, request=request_obj)
            if offer_form.is_valid():
                offer = offer_form.save(commit=False)
                offer.request = request_obj
                offer.fulfiller = request.user
                offer.save()
                
                messages.success(request, 'Your offer has been submitted successfully!')
                return redirect('requests:request_detail', pk=pk)
        else:
            offer_form = RequestOfferForm(request=request_obj)
    
    context = {
        'request_obj': request_obj,
        'offers': offers,
        'offer_form': offer_form,
        'user_offer': user_offer,
        'can_fulfill': request_obj.can_be_fulfilled,
    }
    
    return render(request, 'requests/request_detail.html', context)


@login_required
def request_edit(request, pk):
    """Edit an existing request"""
    request_obj = get_object_or_404(Request, pk=pk)
    
    # Only the requester can edit
    if request_obj.requester != request.user:
        messages.error(request, 'You can only edit your own requests.')
        return redirect('requests:request_detail', pk=pk)
    
    # Can't edit if request is in progress or completed
    if request_obj.status in ['in_progress', 'completed']:
        messages.error(request, 'Cannot edit requests that are in progress or completed.')
        return redirect('requests:request_detail', pk=pk)
    
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=request_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Request updated successfully!')
            return redirect('requests:request_detail', pk=pk)
    else:
        form = RequestForm(instance=request_obj)
    
    return render(request, 'requests/request_form.html', {'form': form, 'action': 'Edit'})


@login_required
def request_delete(request, pk):
    """Delete a request"""
    request_obj = get_object_or_404(Request, pk=pk)
    
    # Only the requester can delete
    if request_obj.requester != request.user:
        messages.error(request, 'You can only delete your own requests.')
        return redirect('requests:request_detail', pk=pk)
    
    # Can't delete if request is in progress or completed
    if request_obj.status in ['in_progress', 'completed']:
        messages.error(request, 'Cannot delete requests that are in progress or completed.')
        return redirect('requests:request_detail', pk=pk)
    
    if request.method == 'POST':
        request_obj.delete()
        messages.success(request, 'Request deleted successfully!')
        return redirect('requests:request_list')
    
    return render(request, 'requests/request_confirm_delete.html', {'request_obj': request_obj})


@login_required
def offer_manage(request, pk):
    """Manage offers for a request (requester only)"""
    request_obj = get_object_or_404(Request, pk=pk)
    
    # Only the requester can manage offers
    if request_obj.requester != request.user:
        messages.error(request, 'You can only manage offers for your own requests.')
        return redirect('requests:request_detail', pk=pk)
    
    offers = request_obj.offers.all().select_related('fulfiller')
    
    context = {
        'request_obj': request_obj,
        'offers': offers,
    }
    
    return render(request, 'requests/offer_manage.html', context)


@login_required
def offer_accept(request, offer_pk):
    """Accept an offer"""
    offer = get_object_or_404(RequestOffer, pk=offer_pk)
    
    # Only the requester can accept offers
    if offer.request.requester != request.user:
        messages.error(request, 'You can only accept offers for your own requests.')
        return redirect('requests:request_detail', pk=offer.request.pk)
    
    # Can only accept offers for open requests
    if offer.request.status != 'open':
        messages.error(request, 'Can only accept offers for open requests.')
        return redirect('requests:request_detail', pk=offer.request.pk)
    
    # Accept the offer
    offer.accept()
    
    # Create fulfillment record
    RequestFulfillment.objects.create(
        request=offer.request,
        offer=offer
    )
    
    messages.success(request, f'Offer from {offer.fulfiller.username} has been accepted!')
    return redirect('requests:request_detail', pk=offer.request.pk)


@login_required
def offer_reject(request, offer_pk):
    """Reject an offer"""
    offer = get_object_or_404(RequestOffer, pk=offer_pk)
    
    # Only the requester can reject offers
    if offer.request.requester != request.user:
        messages.error(request, 'You can only reject offers for your own requests.')
        return redirect('requests:request_detail', pk=offer.request.pk)
    
    offer.reject()
    messages.success(request, f'Offer from {offer.fulfiller.username} has been rejected.')
    return redirect('requests:request_detail', pk=offer.request.pk)


@login_required
def offer_withdraw(request, offer_pk):
    """Withdraw an offer"""
    offer = get_object_or_404(RequestOffer, pk=offer_pk)
    
    # Only the offer maker can withdraw
    if offer.fulfiller != request.user:
        messages.error(request, 'You can only withdraw your own offers.')
        return redirect('requests:request_detail', pk=offer.request.pk)
    
    offer.withdraw()
    messages.success(request, 'Your offer has been withdrawn.')
    return redirect('requests:request_detail', pk=offer.request.pk)


@login_required
def my_requests(request):
    """Display user's own requests"""
    requests_list = Request.objects.filter(requester=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(requests_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_requests': requests_list.count(),
        'open_requests': requests_list.filter(status='open').count(),
        'completed_requests': requests_list.filter(status='completed').count(),
    }
    
    return render(request, 'requests/my_requests.html', context)


@login_required
def my_offers(request):
    """Display user's offers"""
    offers_list = RequestOffer.objects.filter(fulfiller=request.user).select_related('request').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(offers_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_offers': offers_list.count(),
        'pending_offers': offers_list.filter(status='pending').count(),
        'accepted_offers': offers_list.filter(status='accepted').count(),
    }
    
    return render(request, 'requests/my_offers.html', context)


@login_required
def fulfillment_complete(request, fulfillment_pk):
    """Mark fulfillment as completed"""
    fulfillment = get_object_or_404(RequestFulfillment, pk=fulfillment_pk)
    
    # Only the requester can mark as completed
    if fulfillment.request.requester != request.user:
        messages.error(request, 'You can only mark your own requests as completed.')
        return redirect('requests:request_detail', pk=fulfillment.request.pk)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        
        if rating:
            fulfillment.rating = int(rating)
        if review:
            fulfillment.review = review
        
        fulfillment.mark_completed()
        messages.success(request, 'Request marked as completed!')
        return redirect('requests:request_detail', pk=fulfillment.request.pk)
    
    return render(request, 'requests/fulfillment_complete.html', {'fulfillment': fulfillment})


def request_stats(request):
    """Display request statistics"""
    total_requests = Request.objects.count()
    open_requests = Request.objects.filter(status='open').count()
    completed_requests = Request.objects.filter(status='completed').count()
    total_fees = Request.objects.aggregate(total=models.Sum('fee'))['total'] or 0
    
    # Category breakdown
    category_stats = Request.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'total_requests': total_requests,
        'open_requests': open_requests,
        'completed_requests': completed_requests,
        'total_fees': total_fees,
        'category_stats': category_stats,
    }
    
    return render(request, 'requests/request_stats.html', context)
