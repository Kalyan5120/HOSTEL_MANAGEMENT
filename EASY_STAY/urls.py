"""
URL configuration for EASY_STAY project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from EASY_STAY.views import easy_stay_view
from django.conf import settings
from django.conf.urls.static import static

app_name='easy_stay'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(route='',view=easy_stay_view,name='easy_stay'),
    path(route='Customer/',view=include('Customer.urls'),name='Customer'),
    path(route='Owner/',view=include('Owner.urls'),name='Owner')
]


if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
