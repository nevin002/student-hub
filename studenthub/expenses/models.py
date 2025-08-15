from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Expense(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_paid')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    participants = models.ManyToManyField(User, related_name='expenses_shared')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - ${self.amount}"
    
    def per_head(self):
        """Calculate amount per person"""
        participant_count = self.participants.count()
        if participant_count > 0:
            return self.amount / participant_count
        return Decimal('0.00')
    
    @property
    def participant_count(self):
        return self.participants.count()
