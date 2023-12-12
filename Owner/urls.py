from django.urls import path
from Owner.views import owner_view,owner_home_view,logout_view,owner_registration_view,forgetpassword_view,otp_confirm_view,changepswrd_view,owner_pdetails

urlpatterns=[
    path(route='owner_login/',view=owner_view,name='o_login'),
    path(route='owner_logout/',view=logout_view,name='o_logout'),
    path(route='home/',view=owner_home_view,name='home'),
    path(route='owner_register/',view=owner_registration_view,name='o_regsiter'),
    path(route='forgetpswrd/',view=forgetpassword_view,name='forgetpswrd'),
    path(route='owner_otp/<int:pk>/',view=otp_confirm_view,name='owner_otp'),
    path(route='changepswrd/<int:pk>/',view=changepswrd_view,name='changepswrd'),
    path(route='p_details/',view=owner_pdetails,name='p_details')

]