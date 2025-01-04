from django import template
from ..models import Ad,City


register=template.Library()

@register.simple_tag
def total_ads():
    return Ad.active.count()

@register.inclusion_tag('ads/ad/latest.ads.html')
def show_latest_ads(count=10):
    latest_ads=Ad.active.order_by('-publish')[:count]

    return{
        'latest_ads':latest_ads
    }

# @register.inclusion_tag('ads/ad/city.ads.html')

@register.simple_tag()
def filter_ads_by_city(city_name):
    city_ads=Ad.active.filter(city__name=city_name)
    return{
  'city_ads':city_ads,
}
