from django.urls import path
from Customer.views import *
app_name='customer'

urlpatterns=[
    path(route='customer_main/',view=customer_main_view,name='c_main'),
    path(route='customer_register/',view=customer_registration_view,name='c_register'),
    path(route='customer_login/',view=customer_view,name='customer_login'),
    path(route='logout/',view=logout_view,name='logout'),

    path(route='list/',view=customer_list,name='list'),
    path(route='p_details/',view=p_details_view,name='p_details'),
    path(route='forgetpswrd/',view=forgetpassword_view,name='forgetpswrd'),
    path(route='customer_otp/<int:pk>/',view=otp_confirm_view,name='customer_otp'),
    path(route='changepswrd/<int:pk>/',view=changepswrd_view,name='changepswrd'),
    path(route='customer_main/',view=customer_main_view,name='c_main'),
    path(route='hostel_detail/<int:pk>',view=hostel_detail_view,name='hostel_detail'),
    path(route='booking/<hostel>/<room>/<bed>/<data1>/<data2>/<data3>/',view=room_book_view,name='booking'),
    path(route='approved_book/<room>/<bed>/<pk>/',view=approved_room_book_view,name='approved_book'),
    
]
