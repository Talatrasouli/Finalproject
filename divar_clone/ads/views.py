from django.shortcuts import render,redirect,get_object_or_404
from django.forms import modelformset_factory
from .forms import Ad,AdForm, AdImageFormSet,AdImageForm
from .models import AdImage,Ad,Category,City
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from .forms import EmailAdvertisementForm,CommentForm,SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.http import HttpResponse
from django.contrib.postgres.search import SearchVector
from django.db.models import Value, CharField
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import AdFilterForm
from django.utils.text import slugify



AdImageFormSet = modelformset_factory(AdImage, form=AdImageForm, extra=3)
# Create your views here.
@login_required
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

    return render(request, 'ads/ad/create_ad.html', {'ad_form': ad_form, 'formset': formset})



# class AdListView(ListView):
#     queryset=Ad.active.all()
#     context_object_name='ads'
#     paginate_by=3
#     template_name='ads/ad/ad_list.html'

# def gallery_view(request):
#     images = Ad.objects.all()  
#     return render(request, 'ads/ad/ad_list.html', {'images': images})



def ad_list(request,tag_slug=None):
    ads= Ad.active.all().order_by('-publish')
    categories = Category.objects.all()
    cities = City.objects.all()

    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        ads=ads.filter(tags__in=[tag])

   
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category_name = request.GET.get('category')
    status = request.GET.get('status')
    city_name = request.GET.get('city')
    if min_price:
        ads = ads.filter(price__gte=min_price)
    if max_price:
        ads = ads.filter(price__lte=max_price)
    if category_name:
        category = get_object_or_404(Category, name=category_name)
        ads = ads.filter(category=category)
    if status:
        ads = ads.filter(status=status)
    search_query = request.GET.get('q', '')
    if search_query:
        ads = ads.filter(title__icontains=search_query)
    if city_name:
        ads = ads.filter(city__name__iexact=city_name)

    paginator=Paginator(ads,per_page=4)
    page_number = request.GET.get('page', 1)
    try:
       ads = paginator.page(page_number)
    except PageNotAnInteger:
          ads = paginator.page(1)
    except EmptyPage:
       ads=paginator.page(paginator.num_pages)

    

    return render(request, 'ads/ad/ad_list.html',{'ads': ads,
        'categories': categories,
        'cities': cities,'tag':tag,'search_query': search_query})



class OwnerMixin:
    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(owner=self.request.user)
    
class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner=self.request.user
        return super().form_valid(form)

class OwnerAdMixin(OwnerMixin,LoginRequiredMixin,PermissionRequiredMixin):
    model=Ad
    fields=['category','title','slug','overview','price','phone_number','image','city']
    # success_url = reverse_lazy('ads:manage_ad_list')
    success_url = reverse_lazy('ads:manage_ad_list')
    def get_object(self,queryset=None):
        obj=super().get_object(queryset)
        if obj.owner !=self.request.user:
            raise PermissionDenied("you don't have permission")
        return obj
class OwnerAdEditMixin(OwnerAdMixin,OwnerEditMixin):
    template_name='ads/manage/ad/form.html'
    # success_url = reverse_lazy('ads:manage_ad_list')
  


class ManageAdListview(OwnerAdMixin,ListView):
    template_name='ads/manage/ad/list.html'
    permission_required='ads.view_ad'
    ontext_object_name='ads'
    # paginate_by=3
   
  



class AdCreateView(OwnerAdEditMixin,CreateView):
    permission_required = 'ads.add_ad'
    template_name = 'ads/manage/ad/form.html'
    # success_url = reverse_lazy('ads:ad_list')


    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)

class AdUpdateView(OwnerAdEditMixin,UpdateView):
    permission_required='ads.change_ad'
    template_name = 'ads/manage/ad/edit.html'

class AdDeleteView(OwnerAdMixin,DeleteView):
    template_name='ads/manage/ad/delete.html'
    permission_required='ads.delete_ad'

    


@login_required
def ad_detail(request,id):
    ad=get_object_or_404(Ad,id=id,status=Ad.Status.ACTIVE)
    comments=ad.comments.filter(active=True)
    form=CommentForm()
    ad_tag_ids=ad.tags.values_list('id',flat=True)
    similar_ads=Ad.active.filter(tags__in=ad_tag_ids).exclude(id=ad.id)
    similar_ads= similar_ads.annotate(same_tags_acount=Count('tags')).order_by('-same_tags_acount','publish')[:3]
    return render(request,'ads/ad/ad_detail.html',{'ad': ad,'comments':comments,'form':form,'similar_ads':similar_ads})
  


@login_required
def ad_share(request,ad_id):
    ad=get_object_or_404(Ad,id=ad_id,status=Ad.Status.ACTIVE)
    sent=False
    if request.method=='POST':
        form=EmailAdvertisementForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            ad_url=request.build_absolute_uri(
                ad.get_absolute_url()
            )
            subject=f"{cd['name']} recommends you read {ad.title}"
            message=f'''Read {ad.title}  at {ad_url}

               {cd['name']}'s comment:{cd['comment']}
'''         
            send_mail(subject,message,'a@a.com',[cd['to']])
            sent=True
         
    else:
        form=EmailAdvertisementForm()
    return render(request,'ads/ad/share.html',{'ad':ad,'form':form,'sent':sent})

@require_POST
def ad_comment(request,ad_id):
    ad=get_object_or_404(Ad,id=ad_id,status=Ad.Status.ACTIVE)
    comment=None
    form=CommentForm(data=request.POST)
    if form.is_valid():
        comment=form.save(commit=False)
        comment.ad=ad
        comment.save()
    return render(request,'ads/ad/comment.html',{'ad':ad,'form':form,'comment':comment})



@login_required
def city_ads_view(request, city_name):
    ads = Ad.objects.filter(city__name__iexact=city_name)
    context = {
        'city_name': city_name,
        'ads': ads,
    }
    return render(request, 'ads/ad/city.ads.html', context)


@login_required
def ad_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
          
            results = Ad.objects.filter(
                Q(title__icontains=query) |  
                Q(description__icontains=query) |  
                Q(price__icontains=query)  
            )

    return render(request, 'ads/ad/search.html', {'form': form, 'query': query, 'results': results}) 


@login_required
def ad_filter(request):
    form = AdFilterForm()
    query = None
    results = Ad.objects.all()  

    if request.GET: 
        form = AdFilterForm(request.GET)
        if form.is_valid():
            
            query = form.cleaned_data.get('query', None)
            min_price = form.cleaned_data.get('min_price', None)
            max_price = form.cleaned_data.get('max_price', None)
            # status = form.cleaned_data.get('status', None)
            category = form.cleaned_data.get('category', None)
            city = form.cleaned_data.get('city', None)

            
            if query:
                results = results.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query)
                )

            
            if min_price is not None:
                results = results.filter(price__gte=min_price)
            if max_price is not None:
                results = results.filter(price__lte=max_price)


            # if status:
            #     results = results.filter(status=status)

            
            if category:
                results = results.filter(category=category)

            
            if city:
                results = results.filter(city=city)

    return render(request, 'ads/ad/filter.html', {'form': form, 'query': query, 'results': results})