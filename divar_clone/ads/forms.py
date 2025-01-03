from django import forms
from .models import Ad, AdImage,Comment
from django.forms import modelformset_factory

class EmailPostForm(forms.Form):
    name=forms.CharField(max_length=50)
    email=forms.EmailField()
    to=forms.EmailField()
    comment=forms.CharField(required=False,widget=forms.Textarea)

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description']

class AdImageForm(forms.ModelForm):
    class Meta:
        model = AdImage
        fields = ['image']

AdImageFormSet = modelformset_factory(AdImage, form=AdImageForm, extra=3)


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['name','email','body']
        
