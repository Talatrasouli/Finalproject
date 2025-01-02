from django.shortcuts import render,redirect,get_object_or_404
from django.forms import modelformset_factory
from .forms import Ad,AdForm, AdImageFormSet,AdImageForm
from .models import AdImage,Ad,Category
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger



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
    ads= Ad.active.all()
    paginator=Paginator(ads,per_page=4)
    page_number = request.GET.get('page', 1)
    
    try:
       ads = paginator.page(page_number)
    except PageNotAnInteger:
          ads = paginator.page(1)
    except EmptyPage:
       ads=paginator.page(paginator.num_pages)
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category_name = request.GET.get('category')
    status = request.GET.get('status')
    if category_name:
        category = get_object_or_404(Category, name=category_name)
        ads = ads.filter(category=category)
    if status:
        ads = ads.filter(status=status)
    if min_price:
        ads = ads.filter(price__gte=min_price)
    if max_price:
        ads = ads.filter(price__lte=max_price)
    search_query = request.GET.get('q', '')
    if search_query:
        ads = ads.filter(title__icontains=search_query)

    return render(request, 'ads/ad/ad_list.html',{'ads': ads, 'search_query': search_query})


def ad_detail(request,id):
    ad=get_object_or_404(Ad,id=id,status=Ad.Status.ACTIVE)
    return render(request,'ads/ad/ad_detail.html',{'ad': ad})
