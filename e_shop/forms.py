from django import forms
from e_shop.models import ProductReview

class ProductReviewform(forms.ModelForm):
    review = forms.CharField( widget= forms.Textarea(attrs={'placeholder': "Write review"}))
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']