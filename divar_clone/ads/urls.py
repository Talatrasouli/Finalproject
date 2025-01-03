from django.urls import path
from . import views
from .views import create_ad

app_name='ads'

urlpatterns = [

    # path('',views.ad_list,name='ad_list'),
    path('',views.AdListView.as_view(),name='ad_list'),
    path('<int:id>/',views.ad_detail,name='ad_detail'),
    # path('<int:year>/<int:month>/<int:day>/<slug:ad_slug>',views.ad_detail,name='ad_detail')
    path('<int:ad_id>/share/',views.ad_share,name='ad_share'),
    path('<int:ad_id>/comment/',views.ad_comment,name='ad_comment'),
    # path('create_ad/', views.create_ad, name='create_ad'),
    
]