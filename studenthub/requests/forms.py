from django import forms
from django.utils import timezone
from .models import Request, RequestOffer


class RequestForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
            }
        ),
        help_text='Optional: Set a deadline for when you need this request fulfilled'
    )
    
    phone = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1 (555) 123-4567',
            'pattern': r'[\+]?[1-9][\d]{0,15}'
        }),
        help_text='Your phone number for contact (optional)'
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        }),
        help_text='Your email address for contact (optional)'
    )
    
    class Meta:
        model = Request
        fields = [
            'title', 'description', 'category', 'fee', 
            'location', 'deadline', 'is_urgent', 'contact_preference',
            'phone', 'email'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What do you need?'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe what you need in detail...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where do you need this? (optional)'
            }),
            'is_urgent': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'contact_preference': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline <= timezone.now():
            raise forms.ValidationError('Deadline must be in the future.')
        return deadline
    
    def clean_fee(self):
        fee = self.cleaned_data.get('fee')
        if fee <= 0:
            raise forms.ValidationError('Fee must be greater than zero.')
        return fee
    
    def clean(self):
        cleaned_data = super().clean()
        contact_preference = cleaned_data.get('contact_preference')
        phone = cleaned_data.get('phone')
        email = cleaned_data.get('email')
        
        # Validate contact information based on preference
        if contact_preference == 'phone' and not phone:
            raise forms.ValidationError({
                'phone': 'Phone number is required when phone is selected as contact preference.'
            })
        elif contact_preference == 'email' and not email:
            raise forms.ValidationError({
                'email': 'Email address is required when email is selected as contact preference.'
            })
        elif contact_preference == 'both' and not phone and not email:
            raise forms.ValidationError({
                'phone': 'At least one contact method (phone or email) is required when both is selected.',
                'email': 'At least one contact method (phone or email) is required when both is selected.'
            })
        
        return cleaned_data


class RequestOfferForm(forms.ModelForm):
    estimated_delivery = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
            }
        ),
        help_text='Optional: When can you deliver/complete this request?'
    )
    
    class Meta:
        model = RequestOffer
        fields = ['proposed_fee', 'message', 'estimated_delivery']
        widgets = {
            'proposed_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe how you can fulfill this request...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if self.request:
            # Set initial proposed fee to the request fee
            self.fields['proposed_fee'].initial = self.request.fee
            self.fields['proposed_fee'].help_text = f'Request fee: ${self.request.fee}'
    
    def clean_proposed_fee(self):
        proposed_fee = self.cleaned_data.get('proposed_fee')
        if proposed_fee <= 0:
            raise forms.ValidationError('Proposed fee must be greater than zero.')
        return proposed_fee
    
    def clean_estimated_delivery(self):
        estimated_delivery = self.cleaned_data.get('estimated_delivery')
        if estimated_delivery and estimated_delivery <= timezone.now():
            raise forms.ValidationError('Estimated delivery must be in the future.')
        return estimated_delivery


class RequestFilterForm(forms.Form):
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + Request.CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Request.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_fee = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Fee',
            'step': '0.01'
        })
    )
    max_fee = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Fee',
            'step': '0.01'
        })
    )
    is_urgent = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search requests...'
        })
    )
