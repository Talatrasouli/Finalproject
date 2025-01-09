from django.urls import path,include
from rest_framework import routers 
from . import views

app_name='ads'

router=routers.DefaultRouter()
router.register('categories',views.CategoryViewSet)



urlpatterns = [

    path('categories/',views.CategoryListView.as_view(),name='category_list'),
    path('categories/,<pk>/',views.CategoryDetailView.as_view(),name='category_detail'),
    path('ads/',views.AdListView.as_view(),name='ad_list'),
    path('ads/<pk>/',views.AdDetailView.as_view(),name='ad_detail'),
    path('ads/<pk>/enroll',views.AdEnrollView.as_view(),name='ad_enroll'),
    path('',include(router.urls))
   
]
