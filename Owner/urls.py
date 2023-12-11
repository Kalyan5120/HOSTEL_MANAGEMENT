from django.urls import path
from Owner.views import owner_view,owner_home_view,logout_view,owner_registration_view

urlpatterns=[
    path(route='owner_login/',view=owner_view,name='o_login'),
    path(route='owner_logout/',view=logout_view,name='o_logout'),
    path(route='home/',view=owner_home_view,name='home'),
    path(route='owner_register/',view=owner_registration_view,name='o_regsiter'),

]