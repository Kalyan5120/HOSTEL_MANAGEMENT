from django.shortcuts import render,redirect
from Customer.forms import cust_form,customer_login,changepswrd_form,book_room_form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import random
from django.conf import settings
from django.core.mail import send_mail
from Customer.models import customer_register,customer_book
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from Owner.models import hostel_details_model,rooms_details_model,bed_details_model,gallery_model



# Create your views here.



def hostel_detail_view(request,pk):
    res=hostel_details_model.objects.get(hostel_id=pk)
    room=rooms_details_model.objects.filter(hostel_id=pk)
    bed=bed_details_model.objects.all()
    images=gallery_model.objects.all()
    print(res)
    return render(request=request,template_name='hostel_detail.html',context={'hostel':res,'room_details':room,'bed_details':bed,'images':images})





def room_book_view(request,hostel,room,bed,data1,data2,data3):
    print(hostel,room,bed,data1,data2,data3)
    form=book_room_form()
    if request.method=='POST' and request.FILES:
        form=book_room_form(request.POST,request.FILES)
        if form.is_valid():
            data=form.save(commit=False)
            data.hostel_id=hostel
            data.room_id=room
            data.bed_id=bed
            data.approved=False
            print("haii")
            if data:
                form.save()
                subject='Your requesting booking bed'
                msg=f'''hello {form.cleaned_data['first_name']},
                thank your choose my hostel: 
                hostel:{data1}
                room:{data2}
                bedno:{data3}
                thank you.
                
                '''
                send_mail(subject=subject,message=msg,from_email=settings.EMAIL_HOST_USER,recipient_list=[form.cleaned_data['c_email']])
                
                subject1='confirm the booking the room'
                msg=f'''hello ,
                My self {form.cleaned_data['first_name']}
                i am looking for room please Approval the room: 
                hostel:{data.hostel_id},{data1}
                room:{data.room_id},{data2}
                bedno:{data.bed_id},{data3}
                thank you.
                link: http://127.0.0.1:8000/Customer/approved_book/{data.room_id}/{data.bed_id}/{data.id}/
                '''
                send_mail(subject=subject,message=msg,from_email=settings.EMAIL_HOST_USER,recipient_list=[settings.EMAIL_HOST_USER,])
                messages.success("To sent the email approval from owner")
                return redirect('/Customer/home/')
    return render(request=request,template_name='book_room.html',context={'form':form})



def approved_room_book_view(request,room,bed,pk):
    res=bed_details_model.objects.get(bed_id=bed,room_no=room)
    if res:
        bed_details_model.objects.filter(bed_id=bed,room_no=room).update(availability=False)
        customer_book.objects.filter(id=pk).update(approved=True)
        subject='Your bad is approved successfully'
        res=customer_book.objects.get(id=pk)
        msg=f'''hello {res.first_name},
                you can join with in four days.
                thank you.
                '''
        send_mail(subject=subject,message=msg,from_email=settings.EMAIL_HOST_USER,recipient_list=[res.c_email,])
        messages.success(request,"successfully approval")
    else:
        messages.success(request,"approval failed")
    return redirect('/Customer/home/')
    