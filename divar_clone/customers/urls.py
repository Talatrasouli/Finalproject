from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.CustomersRegistrationView.as_view(),name='customer_registration')
]
