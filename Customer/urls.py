from django.urls import path
from Customer.views import customer_registration_view,customer_login,logout_view,home_view
app_name='customer'

urlpatterns=[
    path(route='customer_register/',view=customer_registration_view,name='c_register'),
    path(route='customer_login/',view=customer_login,name='c_login'),
    path(route='logout/',view=logout_view,name='logout'),
    path(route='home/',view=home_view,name='home')
]
