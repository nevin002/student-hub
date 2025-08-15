from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'payer', 'amount', 'participant_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'payer__username')
    date_hierarchy = 'created_at'
    filter_horizontal = ('participants',)
    
    def participant_count(self, obj):
        return obj.participant_count
    participant_count.short_description = 'Participants'
