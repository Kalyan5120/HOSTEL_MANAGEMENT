
from django.shortcuts import render

def easy_stay_view(request):
    return render(request=request,template_name='easystay.html')