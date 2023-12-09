from django.urls import path
from Customer.views import customer_registration_view,customer_view,logout_view,home_view,customer_list,p_details_view
app_name='customer'

urlpatterns=[
    path(route='customer_register/',view=customer_registration_view,name='c_register'),
    path(route='customer_login/',view=customer_view,name='customer_login'),
    path(route='logout/',view=logout_view,name='logout'),
    path(route='home/',view=home_view,name='home'),
    path(route='list/',view=customer_list,name='list'),
    path(route='p_details/',view=p_details_view,name='p_details')
]
