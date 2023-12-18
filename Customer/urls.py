from django.urls import path
from Customer.views import *
app_name='customer'

urlpatterns=[
    path(route='customer_main/',view=customer_main_view,name='c_main'),
    path(route='customer_register/',view=customer_registration_view,name='c_register'),
    path(route='customer_login/',view=customer_view,name='customer_login'),
    path(route='logout/',view=logout_view,name='logout'),
    path(route='home/',view=home_view,name='home'),
    path(route='list/',view=customer_list,name='list'),
    path(route='p_details/',view=p_details_view,name='p_details'),
    path(route='forgetpswrd/',view=forgetpassword_view,name='forgetpswrd'),
    path(route='customer_otp/<int:pk>/',view=otp_confirm_view,name='customer_otp'),
    path(route='changepswrd/<int:pk>/',view=changepswrd_view,name='changepswrd'),
    
]
