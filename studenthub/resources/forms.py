from django import forms
from .models import Resource, Comment
from .models import Tag


class ResourceForm(forms.ModelForm):
    tag_list = forms.CharField(
        max_length=200,
        required=False,
        help_text='Enter tags separated by commas (e.g., python, django, tutorial)',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Resource
        fields = ['title', 'link', 'file', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def save(self, commit=True):
        resource = super().save(commit=False)
        if commit:
            resource.save()
            # Handle tags
            tag_list = self.cleaned_data.get('tag_list', '')
            if tag_list:
                tags = [tag.strip() for tag in tag_list.split(',') if tag.strip()]
                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                    resource.tags.add(tag)
        return resource


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment...'}),
        }
