from django.urls import path
from . import views
from .views import create_ad


app_name='ads'

urlpatterns = [

    path('',views.ad_list,name='ad_list'),
    # path('',views.AdListView.as_view(),name='ad_list'),
    path('tag/<slug:tag_slug>/',views.ad_list,name='ad_list_by_tag'),
    path('<int:id>/',views.ad_detail,name='ad_detail'),
    # path('<int:year>/<int:month>/<int:day>/<slug:ad_slug>',views.ad_detail,name='ad_detail')
    path('<int:ad_id>/share/',views.ad_share,name='ad_share'),
    path('<int:ad_id>/comment/',views.ad_comment,name='ad_comment'),
    path('city/<str:city_name>/', views.city_ads_view, name='city_ads_view'),
    path('search/',views.ad_search,name='ad_search'),
    path('filter/',views.ad_filter,name='ad_filter'),
    path('create_ad/', views.create_ad, name='create_ad'),
    path('mine/',
         views.ManageAdListview.as_view(),
         name='manage_ad_list'),
   
    path('create/',
         views.AdCreateView.as_view(),
         name='ad_create'),
    path('<pk>/edit/',
         views.AdUpdateView.as_view(),
         name='ad_edit'),
    path('<pk>/delete/',
         views.AdDeleteView.as_view(),
         name='ad_delete'),
    
]