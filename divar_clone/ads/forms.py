from django import forms
from .models import Ad, AdImage
from django.forms import modelformset_factory

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description']

class AdImageForm(forms.ModelForm):
    class Meta:
        model = AdImage
        fields = ['image']

AdImageFormSet = modelformset_factory(AdImage, form=AdImageForm, extra=3)