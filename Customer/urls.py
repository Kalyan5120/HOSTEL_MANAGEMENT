from django.urls import path
from Customer.views import *
app_name='customer'

urlpatterns=[
   

    path(route='hostel_detail/<int:pk>',view=hostel_detail_view,name='hostel_detail'),
    path(route='booking/<hostel>/<room>/<bed>/<data1>/<data2>/<data3>/',view=room_book_view,name='booking'),
    path(route='approved_book/<room>/<bed>/<pk>/',view=approved_room_book_view,name='approved_book'),
    
]
