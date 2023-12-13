from django.urls import path
from Owner.views import owner_view,owner_home_view,logout_view,owner_registration_view,forgetpassword_view,otp_confirm_view,changepswrd_view,hostel_details_view,gallery_view,comments_view,room_details_view,bed_details_view,occupied_details_view,list_view

app_name='owner'

urlpatterns=[
    path(route='owner_login/',view=owner_view,name='o_login'),
    path(route='owner_logout/',view=logout_view,name='o_logout'),
    path(route='home/',view=owner_home_view,name='home'),
    path(route='owner_register/',view=owner_registration_view,name='o_regsiter'),
    path(route='forgetpswrd/',view=forgetpassword_view,name='forgetpswrd'),
    path(route='owner_otp/<int:pk>/',view=otp_confirm_view,name='owner_otp'),
    path(route='changepswrd/<int:pk>/',view=changepswrd_view,name='changepswrd'),
    path(route='hostel_details/',view=hostel_details_view,name='hostel_details'),
    path(route='gallery/',view=gallery_view,name='gallery'),
    path(route='comments/',view=comments_view,name='comments'),
    path(route='room_details/',view=room_details_view,name='room_details'),
    path(route='bed_details/<int:pk>/',view=bed_details_view,name='bed_details'),
    path(route='occupied_details/',view=occupied_details_view,name='occupied_details'),
    path(route='list/',view=list_view,name='list')
]