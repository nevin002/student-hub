from django.contrib import admin
from .models import Request, RequestOffer, RequestFulfillment


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'requester', 'category', 'fee', 'status', 
        'is_urgent', 'location', 'created_at'
    ]
    list_filter = [
        'status', 'category', 'is_urgent', 'contact_preference',
        'created_at', 'deadline'
    ]
    search_fields = ['title', 'description', 'requester__username', 'location']
    date_hierarchy = 'created_at'
    list_editable = ['status', 'is_urgent']
    readonly_fields = ['created_at', 'updated_at', 'total_offers']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'fee', 'requester')
        }),
        ('Location & Timing', {
            'fields': ('location', 'deadline', 'is_urgent')
        }),
        ('Contact Information', {
            'fields': ('contact_preference', 'phone', 'email'),
            'description': 'Provide contact details based on preference'
        }),
        ('Status & Metadata', {
            'fields': ('status', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_offers(self, obj):
        return obj.total_offers
    total_offers.short_description = 'Total Offers'


@admin.register(RequestOffer)
class RequestOfferAdmin(admin.ModelAdmin):
    list_display = [
        'request', 'fulfiller', 'proposed_fee', 'status', 
        'estimated_delivery', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'estimated_delivery']
    search_fields = [
        'request__title', 'fulfiller__username', 'message'
    ]
    date_hierarchy = 'created_at'
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Offer Details', {
            'fields': ('request', 'fulfiller', 'proposed_fee', 'message')
        }),
        ('Timing', {
            'fields': ('estimated_delivery',)
        }),
        ('Status & Metadata', {
            'fields': ('status', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RequestFulfillment)
class RequestFulfillmentAdmin(admin.ModelAdmin):
    list_display = [
        'request', 'fulfiller', 'completion_date', 'rating', 
        'created_at'
    ]
    list_filter = ['rating', 'completion_date', 'created_at']
    search_fields = [
        'request__title', 'fulfiller__username', 'review'
    ]
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Fulfillment Details', {
            'fields': ('request', 'offer', 'fulfiller')
        }),
        ('Completion & Review', {
            'fields': ('completion_date', 'rating', 'review')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
