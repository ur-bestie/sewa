# forms.py
from django import forms
from userapp.models import House, HousePicture
from multiupload.fields import MultiFileField

class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['name', 'location', 'price', 'description', 'features', 'main_picture']

    # No need for widget anymore, Django will handle the field for us
    other_pictures = MultiFileField(required=False)