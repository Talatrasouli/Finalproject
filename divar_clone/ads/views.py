from django.shortcuts import render,redirect
from .forms import AdForm, AdImageFormSet
from .models import Ad,AdImage

# Create your views here.
def create_ad(request):
    if request.method == 'POST':
        ad_form = AdForm(request.POST)
        formset = AdImageFormSet(request.POST, request.FILES, queryset=AdImage.objects.none())

        if ad_form.is_valid() and formset.is_valid():
            ad = ad_form.save()  # ذخیره آگهی

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    AdImage.objects.create(ad=ad, image=image)  # ذخیره تصاویر

            return redirect('ad_list')  # یا هر صفحه‌ای که نیاز دارید
    else:
        ad_form = AdForm()
        formset = AdImageFormSet(queryset=AdImage.objects.none())

    return render(request, 'create_ad.html', {'ad_form': ad_form, 'formset': formset})