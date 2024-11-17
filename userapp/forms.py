from django import forms
from .models import HousePurchaseInfo

class HousePurchaseForm(forms.ModelForm):
    class Meta:
        model = HousePurchaseInfo
        fields = '__all__'
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }
