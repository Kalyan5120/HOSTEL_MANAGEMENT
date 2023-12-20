from django.urls import path
from Owner.views import *

app_name='owner'

urlpatterns=[
    path(route='owner_main/',view=owner_main_view,name='o_main'),

    path(route='owner_register/',view=owner_registration_view,name='owner_register'),
    path(route='owner_login/',view=owner_view,name='owner_login'),
    path(route='owner_logout/',view=logout_view,name='owner_logout'),

    path(route='home/',view=owner_home_view,name='home'),

    path(route='forgetpswrd/',view=forgetpassword_view,name='forgetpswrd'),
    path(route='owner_otp/<int:pk>/<email>/',view=otp_confirm_view,name='owner_otp'),
    path(route='changepswrd/<int:pk>/',view=changepswrd_view,name='changepswrd'),

    path(route='hostel_details/',view=hostel_details_view,name='hostel_details'),
    path(route='myhostels/',view=my_hostel_details,name='myhostels'),
    path(route='hostel_list/<int:pk>/',view=room_list_view,name='hostel_list'),
    path(route='hostel_update/<int:pk>/',view=hostel_update_view,name='hostel_update'),
    path(route='hostel_delete/<int:pk>/',view=hostel_delete_view,name='hostel_delete'),

    path(route='gallery/<int:pk>/',view=gallery_view,name='gallery'),
    path(route='gallery_images/<int:pk>/',view=gallery_list_view,name='gallery_images'),
    path(route='delete_images/<int:pk>/',view=gallery_delete_view,name='delete_images'),
    path(route='comments/',view=comments_view,name='comments'),

    path(route='room_details/',view=room_details_view,name='room_details'),
    path(route='room_update/<int:pk>/',view=room_update_view,name='room_update'),
    path(route='room_delete/<int:pk>/',view=room_delete_view,name='room_delete'),

    path(route='bed_details/<int:pk>/',view=bed_details_view,name='bed_details'),
    path(route='bed_update/<int:pk>/',view=update_bed_view,name='bed_update'),
    path(route='bed_delete/<int:pk>/',view=delete_bed_view,name='bed_delete'),

    path(route='occupied_details/',view=occupied_details_view,name='occupied_details'),
    path(route='occ_update/<int:pk>/',view=occupied_update_view,name='occ_update'),

    path(route='list/',view=list_view,name='list'),
    path(route='availability/',view=availability_view,name='availability'),
    path(route='booking/<hostel>/<room>/<bed>/<data1>/<data2>/<data3>/',view=owner_book_view,name='booking'),

    path(route='index/',view=index,name='index'),

    

]