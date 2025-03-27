from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'form__textarea', 'placeholder': 'Review'}),
            'rating': forms.NumberInput(attrs={'class': 'form__slider-value', 'min': '0', 'max': '10', 'step': '0.1'}),
        }

class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    quoted_comment_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form__textarea', 'placeholder': 'Add comment'})
        }
