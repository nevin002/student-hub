from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone


class Request(models.Model):
    CATEGORY_CHOICES = [
        ('books', 'Books'),
        ('electronics', 'Electronics'),
        ('food', 'Food & Drinks'),
        ('transport', 'Transport'),
        ('services', 'Services'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    CONTACT_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('both', 'Both'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    location = models.CharField(max_length=200, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_urgent = models.BooleanField(default=False)
    contact_preference = models.CharField(max_length=10, choices=CONTACT_CHOICES, default='email')
    phone = models.CharField(max_length=20, blank=True, help_text="Your phone number for contact")
    email = models.EmailField(blank=True, help_text="Your email address for contact")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.requester.username}"
    
    @property
    def total_offers(self):
        return self.offers.count()
    
    @property
    def can_be_fulfilled(self):
        return self.status == 'open'
    
    def get_contact_info(self):
        """Return appropriate contact information based on preference"""
        if self.contact_preference == 'phone' and self.phone:
            return f"Phone: {self.phone}"
        elif self.contact_preference == 'email' and self.email:
            return f"Email: {self.email}"
        elif self.contact_preference == 'both':
            contact_info = []
            if self.phone:
                contact_info.append(f"Phone: {self.phone}")
            if self.email:
                contact_info.append(f"Email: {self.email}")
            return " | ".join(contact_info) if contact_info else "No contact info provided"
        else:
            return "No contact info provided"


class RequestOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='offers')
    fulfiller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers_made')
    proposed_fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    message = models.TextField()
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['request', 'fulfiller']
    
    def __str__(self):
        return f"Offer by {self.fulfiller.username} for {self.request.title}"
    
    def accept(self):
        """Accept this offer and update request status"""
        self.status = 'accepted'
        self.save()
        
        # Reject all other offers for this request
        RequestOffer.objects.filter(
            request=self.request,
            status='pending'
        ).exclude(pk=self.pk).update(status='rejected')
        
        # Update request status
        self.request.status = 'in_progress'
        self.request.save()
        
        # Create fulfillment record
        RequestFulfillment.objects.create(
            request=self.request,
            offer=self,
            fulfiller=self.fulfiller
        )
    
    def reject(self):
        """Reject this offer"""
        self.status = 'rejected'
        self.save()
    
    def withdraw(self):
        """Withdraw this offer"""
        self.status = 'withdrawn'
        self.save()


class RequestFulfillment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='fulfillments')
    offer = models.ForeignKey(RequestOffer, on_delete=models.CASCADE, related_name='fulfillment')
    fulfiller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fulfillments')
    completion_date = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Fulfillment of {self.request.title} by {self.fulfiller.username}"
    
    def mark_completed(self):
        """Mark this fulfillment as completed"""
        self.completion_date = timezone.now()
        self.save()
        
        # Update request status
        self.request.status = 'completed'
        self.request.save()
