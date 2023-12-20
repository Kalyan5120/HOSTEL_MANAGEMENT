from django.shortcuts import render,redirect
from Owner.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from Owner.models import *
import re
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User



def owner_registration_view(request):
    form=Owner_registration_form()
    if request.method=='POST':
        form=Owner_registration_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/Owner/owner_login')
    return render(request=request,template_name='owner_registration.html',context={'form':form})


def owner_view(request):
    form=Owner_login()
    if request.method=='POST':
        form=Owner_login(request.POST)
        if form.is_valid():
            user=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
        if user:
            login(request,user)
            return redirect('/Owner/home')
    return render(request=request,template_name='owner_login.html',context={'form':form})


@login_required(login_url='/Owner/owner_login')
def logout_view(request):
    logout(request)
    print(request.user)
    return redirect('/Owner/owner_login')


@login_required(login_url='/Owner/owner_login')
def owner_home_view(request):
    return render(request=request,template_name='home_page.html')


#forget password 
def forgetpassword_view(request):
    res=User.objects.all().values_list('email')    
    if request.method=='POST':
        print(request.POST)
        otp=random.randint(0000,9999)
        email=request.POST['email']
        otp_model.objects.filter(username=email).delete()
        otp_model.objects.create(username=email,otp_no=otp)
        print(email,otp)
        print(res)
        if (email,) in res:
            subject='confirm the OTP'
            msg=f'''hello ,
                please confirm the otp:{otp}
                thank you.'''
            send_mail(subject=subject,message=msg,from_email=settings.EMAIL_HOST_USER,recipient_list=[email,])
            email_id=User.objects.get(email=email)
            return redirect(f'/Owner/owner_otp/{email_id.id}/{email}')
        else:
            messages.error(request,'email is incorrect')
    return render(request=request,template_name='forget_password.html')


def otp_confirm_view(request,pk,email):
    if request.method=='POST':
        otp_confirm=otp_model.objects.get(username=email).otp_no
        if str(otp_confirm)==str(request.POST['otp_confirm']):
            otp_confirm=otp_model.objects.get(username=email).delete()
            return redirect(f'/Owner/changepswrd/{pk}/')
        else:
            return redirect('/Owner/forgetpswrd')
    return render(request=request,template_name='enter_otp.html')
    

def changepswrd_view(request,pk):
    form=changepswrd_form()
    if request.method=='POST':
        res=Owner_registration_model.objects.get(id=pk)
        form=changepswrd_form(request.POST)
        if form.is_valid():
            if form.cleaned_data['enter_new_password']==form.cleaned_data['reenter_new_password']:
                Owner_registration_model.objects.filter(id=pk).update(password=make_password(form.cleaned_data['enter_new_password']))
                return redirect('/Owner/owner_login')
    return render(request=request,template_name='change_pswrd.html',context={'form':form})


#hostel_details CRUD operations
@login_required(login_url='/Owner/owner_login')
def hostel_details_view(request):
    form=hostel_details_form()
    if request.method=='POST':
        form=hostel_details_form(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.owner_id=request.user.id
            data.hostel_owner_name=request.user.first_name
            if data:
                form.save()
                return redirect('/Owner/room_details')
    return render(request=request,template_name='hostel_details.html',context={'form':form})


@login_required(login_url='/Owner/owner_login')
def hostel_update_view(request,pk):
    form=hostel_details_model.objects.get(hostel_id=pk)
    if request.method=='POST':
        print(request.user.id,pk)
        form=hostel_details_model.objects.filter(owner_id=request.user.id,hostel_id=pk).update(hostel_name=request.POST['name'],
                                                                                               type_of_hostel=request.POST['type_of_hostel'],
                                                                                               owner_email=request.POST['email'],                                                                   owner_phone_no=request.POST['phone_no'])
        messages.success(request,"Data is updated")
        return redirect('/Owner/myhostels/')
    return render(request=request,template_name='hostel_update.html',context={'form':form})

@login_required(login_url='/Owner/owner_login')
def hostel_delete_view(request,pk):
    form=hostel_details_model.objects.get(hostel_id=pk)
    if request.method=='POST':
        form=hostel_details_model.objects.filter(owner_id=request.user.id,hostel_id=pk).delete()
        messages.success(request,"Hostel is deleted")
        return redirect('/Owner/myhostels/')
    return render(request=request,template_name='hostel_delete_confirm.html',context={'hostel':form})



def gallery_view(request,pk):
    form=gallery_form()
    if request.method=='POST' and request.FILES:
        form=gallery_form(request.POST,request.FILES)
        if form.is_valid():
            data=form.save(commit=False)
            data.hostel_id=pk
            if data:
                form.save()
                messages.success(request,'Image is uploaded')
            else:
                messages.warning(request,'Image is not uploaded')
    return render(request=request,template_name='gallery.html',context={'form':form})


def gallery_list_view(request,pk):
    res=gallery_model.objects.filter(hostel_id=pk)
    return render(request=request,template_name='gallery_images.html',context={'images':res})

    

def gallery_delete_view(request,pk):
        gallery_model.objects.filter(gallery_id=pk).delete()
        messages.success(request,'Image is deleted')
        return HttpResponse('image deleted')

def comments_view(request):
    form=comments_form()
    if request.method=='POST':
        form=comments_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('/Owner/home')
    return render(request=request,template_name='comments.html',context={'form':form})

 # ============== room_details CRUD operations ===============
@login_required(login_url='/Owner/owner_login')
def room_details_view(request):
    form=room_details_form(hostel=request.user.id)
    if request.method=='POST':
        form=room_details_form(request.POST,hostel=request.user.id)
        if form.is_valid():
            form.save()
            hostel_id=form.cleaned_data['hostel_id'].hostel_id
            return redirect(f'/Owner/bed_details/{hostel_id}/')
    return render(request=request,template_name='room_details.html',context={'form':form})

def room_update_view(request,pk):
    res=rooms_details_model.objects.get(room_id=pk)
    form=room_update_form(hostel=request.user.id,instance=res)
    if request.method=='POST':
        res=rooms_details_model.objects.get(room_id=pk)
        form=room_update_form(request.POST,hostel=request.user.id,instance=res)
        if form.is_valid():
            form.save()
            hostel_id=form.cleaned_data['hostel_id'].hostel_id
            return redirect(f'/Owner/hostel_list/{hostel_id}/')
    return render(request=request,template_name='room_details.html',context={'form':form})


def room_delete_view(request,pk):
    res=rooms_details_model.objects.get(room_id=pk)
    if request.method=='POST':
        temp=bed_details_model.objects.filter(room_no_id=pk).values_list('availability')
        if (False,) not in temp:
            res=rooms_details_model.objects.get(room_id=pk).delete()
            messages.success(request,'Room Deleted')
        else:
            messages.warning(request,'All bads should be available')
        return redirect(f'/Owner/myhostels')
    return render(request=request,template_name='room_delete_confirm.html',context={'room':res})



def list_view(request):
    hostel_details=hostel_details_model.objects.all()
    room_details=rooms_details_model.objects.all()
    bed_details=bed_details_model.objects.all()
    return render(request=request,template_name='list.html',context={'hostel_details':hostel_details,'room_details':room_details,'bed_details':bed_details})

@login_required(login_url='/Owner/owner_login')
def room_list_view(request,pk):
    hostel_details=hostel_details_model.objects.get(hostel_id=pk)
    room_details=rooms_details_model.objects.filter(hostel_id_id=pk)
    bed_details=bed_details_model.objects.all()
    return render(request=request,template_name='room_list.html',context={'hostel_details':hostel_details,'room_details':room_details,'bed_details':bed_details})

def availability_view(request):
    res= hostel_details_model.objects.filter(owner_id=request.user.id)
    #total no of beds
    count=[(i.hostel_id,sum([j.num_of_beds for j in rooms_details_model.objects.filter(hostel_id=i)])) for i in res]
    #total no of created:
    
    temp=[(i.hostel_id,sum([bed_details_model.objects.filter(room_no=j).count() for j in rooms_details_model.objects.filter(hostel_id=i)])) for i in res]

    print('total beds','created', "not created",sep='|')
    l=[(k[0][0],k[0][1],k[1][1],(k[0][1])-(k[1][1])) for k in zip(count,temp) if k[0][0]==k[1][0]]
    # print(l)
        
    # total booked bed:

    # bed=bed_details_model.objects.filter(bed_id=)
    # for k in res:
    #     booking=0
    #     booked=0
    #     for j in rooms_details_model.objects.filter(hostel_id=k):
    #         for t in bed_details_model.objects.filter(room_no=j):
    #             print(t,t.availability)
    #             if t.availability:
    #                 booking+=1
    #             else:
    #                 booked+=1
    #         print(booking,booked)
    #         booked,booking=0,0
    #         print('-------------')

    res= hostel_details_model.objects.filter(owner_id=request.user.id)
    booking=0
    booked=0
    l=[]
    for k in res:
        for j in rooms_details_model.objects.filter(hostel_id=k):
            for t in bed_details_model.objects.filter(room_no=j):
                if t.availability:
                    booking+=1
                else:
                    booked+=1
        l+=(k,booking,booked)
        booking,booked=0,0
    print(l)




    



    





# ======== room_details CRUD operations =============


#======== bed_details CRUD operations ===========

def bed_details_view(request,pk):
    form=bed_details_form(hostel=pk)
    if request.method=='POST':
        form=bed_details_form(request.POST,hostel=pk)
        if form.is_valid():
            form.save()
            return redirect('/Owner/home/')

    return render(request=request,template_name='bed_details.html',context={'form':form,'hostel_id':pk})


def update_bed_view(request,pk):
    form=bed_update_form(instance=bed_details_model.objects.get(bed_id=pk))
    if request.method=='POST':
        form=bed_update_form(request.POST,instance=bed_details_model.objects.get(bed_id=pk))
        if form.is_valid():
            form.save()
            messages.success(request,'Bed details updated')
            return redirect('/Owner/myhostels')
    return render(request=request,template_name='update_bed.html',context={'form':form})


def delete_bed_view(request,pk):
    res=bed_details_model.objects.get(bed_id=pk)
    if request.method=='POST':
        res=bed_details_model.objects.get(bed_id=pk)
        if res.availability==True:
            res=bed_details_model.objects.get(bed_id=pk).delete()
            messages.success(request,'Bed details deleted')
        else:
            messages.warning(request,'Bed is not available')
        return redirect('/Owner/myhostels')
    return render(request=request,template_name='bed_delete_confirm.html',context={'Bed':res})


#======== bed_details CRUD operations end ===========


#======== occupied_details CRUD operations ===========

def occupied_details_view(request):
    form=occupied_details_form()
    if request.method=='POST':
        form=occupied_details_form(request.POST)
    return render(request=request,template_name='occupied_details.html',context={'form':form})

def occupied_update_view(request,pk):
    form=occupied_details_form(instance=occupied_details_model.objects.get(occ_id=pk))
    if request.method=='POST':
        form=occupied_details_form(request.POST,instance=occupied_details_model.objects.get(occ_id=pk))
        if form.is_valid():
            form.save()
            return HttpResponse('data is updated')
        else:
            return HttpResponse('data is not updated')
    return render(request=request,template_name='occupied_update.html',context={'form':form})

#======== occupied_details CRUD operations end ===========


def owner_main_view(request):
    return render(request=request,template_name='owner_main.html')


@login_required(login_url='/Owner/owner_login')
def my_hostel_details(request):
    res=hostel_details_model.objects.filter(owner_id=request.user.id)
    temp=gallery_model.objects.all()

    
    hostel= hostel_details_model.objects.filter(owner_id=request.user.id)
    #total no of beds
    count=[(i.hostel_id,sum([j.num_of_beds for j in rooms_details_model.objects.filter(hostel_id=i)])) for i in hostel]
    #total no of created:
    
    count1=[(i.hostel_id,sum([bed_details_model.objects.filter(room_no=j).count() for j in rooms_details_model.objects.filter(hostel_id=i)])) for i in hostel]

    print('total beds','created', "not created",sep='|')
    l=[(k[0][0],k[0][1],k[1][1],(k[0][1])-(k[1][1])) for k in zip(count,count1) if k[0][0]==k[1][0]]
    return render(request,template_name='myhostel.html',context={'hostel_details':res,'images':temp,'available':l})






def owner_book_view(request,hostel,room,bed,data1,data2,data3):
    if request.method=="POST":
        subject='Your requesting booking bed'
        msg=f'''hello {request.POST['username']},
                hostel:{data1}
                room:{data2}
                bedno:{data3}
                please fill the form for further details.
                http://127.0.0.1:8000/Customer/booking/{hostel}/{room}/{bed}/{data1}/{data2}/{data3}/
                thank you.
                '''
        send_mail(subject=subject,message=msg,from_email=settings.EMAIL_HOST_USER,recipient_list=[request.POST['email']])
        messages.success(request,"sent the request mail")
        return redirect('/Customer/home/')
    return render(request,template_name='booking_request.html')
    

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


def index(request):
    return render(request,template_name='index.html')
    