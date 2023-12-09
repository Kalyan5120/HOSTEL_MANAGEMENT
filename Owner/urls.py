from django.urls import path
from Owner.views import Owner_login,logout_view
app_name='Owner'



urlpatterns=[
    path(route='login/',view=Owner_login,name='login'),
    path(route='logout/',view=logout_view,name='logout')
]