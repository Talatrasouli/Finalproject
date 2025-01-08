from django import forms
from .models import Ad, AdImage,Comment,Category,City
from django.forms import modelformset_factory

class EmailAdvertisementForm(forms.Form):
    name=forms.CharField(max_length=50)
    email=forms.EmailField()
    to=forms.EmailField()
    comment=forms.CharField(required=False,widget=forms.Textarea)


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category','title','slug','description', 'price', 'phone_number','image','city']

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.owner = self.current_user
        return super().save(commit=commit)
    

class AdImageForm(forms.ModelForm):
    class Meta:
        model = AdImage
        fields = ['image']

        
AdImageFormSet = modelformset_factory(
    AdImage,
    fields=('image',),
    extra=3  
)


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['name','email','body']
        
class SearchForm(forms.Form):
    query=forms.CharField()


class AdFilterForm(forms.Form):
    query = forms.CharField(required=False, label="filter", widget=forms.TextInput(attrs={'placeholder': 'filter ads...'}))
    min_price = forms.DecimalField(required=False, label="Min Price", min_value=0)
    max_price = forms.DecimalField(required=False, label="Max Price", min_value=0)
    # status = forms.ChoiceField(
    #     required=False,
    #     choices=[
    #         ('', 'All'),
    #         ('new', 'New'),
    #         ('used', 'Used'),
    #     ],
    #     label="Status",
    # )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Category"
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        label="City"
    )

