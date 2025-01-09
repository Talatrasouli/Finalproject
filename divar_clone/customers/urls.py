from django.urls import path
from . import views


app_name = 'customers'

urlpatterns = [
    path('register/',
         views.CustomerRegistrationView.as_view(),
         name='customer_registration')
]