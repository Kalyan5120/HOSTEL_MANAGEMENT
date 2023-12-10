from django.urls import path
from Owner.views import owner_view

urlpatterns=[
    path(route='owner_login/',view=owner_view,name='o_login'),
    # path(route='owner_logout/',view=logout_view,name='o_logout'),
    # path(route='home/',view=home_view,name='home')
]