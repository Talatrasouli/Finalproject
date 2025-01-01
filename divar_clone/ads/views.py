from django.shortcuts import render,redirect,get_object_or_404
from django.forms import modelformset_factory
from .forms import Ad,AdForm, AdImageFormSet,AdImageForm
from .models import AdImage



AdImageFormSet = modelformset_factory(AdImage, form=AdImageForm, extra=3)
# Create your views here.
def create_ad(request):
    if request.method == 'POST':
        ad_form = AdForm(request.POST)
        formset = AdImageFormSet(request.POST, request.FILES, queryset=AdImage.objects.none())

        if ad_form.is_valid() and formset.is_valid():
            ad = ad_form.save()  
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    AdImage.objects.create(ad=ad, image=image)  

            return redirect('ad_list')  
    else:
        ad_form = AdForm()
        formset = AdImageFormSet(queryset=AdImage.objects.none())

    return render(request, 'ads/create_ad.html', {'ad_form': ad_form, 'formset': formset})

def ad_list(request):
    ads = Ad.active.all()
    return render(request, 'ads/ad/ad_list.html', {'ads': ads})

def ad_detail(request,id):
    ad=get_object_or_404(Ad,id=id,status=Ad.status.ACTIVE)
    # try:
    #     ad=Ad.active.get(id=id)
    # except Ad.DoesNotExist:
    #     raise Http404('No Advertisement fount.')
    return render(request,'ads/ad/detail.html',{'ad': ad})
