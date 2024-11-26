from django import forms
from .models import HousePurchaseInfo, housebuy, RentalApplication

class HousePurchaseInfoForm(forms.ModelForm):
    class Meta:
        model = HousePurchaseInfo
        fields = [
            'full_name', 'id_number', 'ssn', 
            'current_address', 'phone', 'email', 
            'monthly_income', 'bank_statements', 'credit_score',
            'employer_name', 'job_title', 'employment_duration_years',
            'property_address', 'property_price', 'comments'
        ]
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
        }


class RentalApplicationForm(forms.ModelForm):
    class Meta:
        model = RentalApplication
        fields = [
            'previous_rental_address',
            'landlord_name',
            'landlord_contact',
            'reason_for_moving',
            'job_title',
            'employer_name',
            'employer_contact',
            'income',
            'consent'
        ]
        widgets = {
            'reason_for_moving': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'previous_rental_address': 'Previous Rental Address',
            'landlord_name': 'Landlord Name',
            'landlord_contact': 'Landlord Contact',
            'reason_for_moving': 'Reason for Moving',
            'job_title': 'Job Title',
            'employer_name': 'Employer Name',
            'employer_contact': 'Employer Contact',
            'income': 'Monthly Income',
            'consent': 'I agree to the terms and conditions'
        }
