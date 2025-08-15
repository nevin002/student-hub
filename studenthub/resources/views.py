from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Resource, Comment, Tag
from .forms import ResourceForm, CommentForm


def resource_list(request):
    resources = Resource.objects.annotate(
        upvote_count=Count('upvotes'),
        comment_count=Count('comments')
    ).order_by('-created_at')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        resources = resources.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(resources, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'resources/resource_list.html', context)


def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    comments = resource.comments.all()
    comment_form = CommentForm()
    
    context = {
        'resource': resource,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'resources/resource_detail.html', context)


@login_required
def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.author = request.user
            resource.save()
            form.save()  # Save tags
            messages.success(request, 'Resource created successfully!')
            return redirect('resources:resource_detail', pk=resource.pk)
    else:
        form = ResourceForm()
    
    context = {
        'form': form,
        'title': 'Create New Resource',
    }
    return render(request, 'resources/resource_form.html', context)


@login_required
def add_comment(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.resource = resource
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment.')
    
    return redirect('resources:resource_detail', pk=pk)


@login_required
def toggle_upvote(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    user = request.user
    
    if user in resource.upvotes.all():
        resource.upvotes.remove(user)
        messages.info(request, 'Upvote removed.')
    else:
        resource.upvotes.add(user)
        messages.success(request, 'Resource upvoted!')
    
    return redirect('resources:resource_detail', pk=pk)
