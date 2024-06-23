from django import forms
from .models import PetInfo

class PetInfoForm(forms.ModelForm):
    class Meta:
        model = PetInfo
        fields = '__all__'
