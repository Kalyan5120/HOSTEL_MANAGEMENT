
from django.shortcuts import render
from Owner.models import hostel_details_model,bed_details_model,rooms_details_model

def easy_stay_view(request):
    res=hostel_details_model.objects.all()
    hostel= hostel_details_model.objects.all()
    booking=0
    booked=0
    l=[]
    for k in hostel:
        for j in rooms_details_model.objects.filter(hostel_id=k):
            for t in bed_details_model.objects.filter(room_no=j):
                if t.availability:
                    booking+=1
                else:
                    booked+=1
        l+=[(k,booking,booked)]
        booking,booked=0,0
    return render(request=request,template_name='easystay.html',context={'hostels':res,'available':l})