from django.shortcuts import render,redirect
from Owner.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from Owner.models import Owner_registration_model,hostel_details_model,occupied_details_model,gallery_model,comments_model,rooms_details_model,bed_details_model
import re
from django.contrib.auth.hashers import make_password



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

otp_confirm=None


def forgetpassword_view(request):
    res=Owner_registration_model.objects.all().values_list('email')    
    global otp_confirm
    if request.method=='POST':
        otp=random.randint(0000,9999)
        otp_confirm=otp
        email=request.POST['email']
        if (email,) in res:
            subject='confirm the OTP'
            msg=f'''hello ,
                please confirm the otp:{otp}
                thank you.'''
            send_mail(subject=subject,message=msg,from_email=settings.EMAIL_HOST_USER,recipient_list=[email,])
            email_id=Owner_registration_model.objects.get(email=email)
            return redirect(f'/Owner/owner_otp/{email_id.id}/')
        else:
            messages.error(request,'email is incorrect')
    return render(request=request,template_name='forget_password.html')


def otp_confirm_view(request,pk):
    if request.method=='POST':
        if str(otp_confirm)==str(request.POST['otp_confirm']):
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



def gallery_view(request):
    form=gallery_form()
    if request.method=='POST' and request.FILES:
        form=gallery_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('/Owner/home')
    return render(request=request,template_name='gallery.html',context={'form':form})


def comments_view(request):
    form=comments_form()
    if request.method=='POST':
        form=comments_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('/Owner/home')
    return render(request=request,template_name='comments.html',context={'form':form})


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
            return redirect(f'/Owner/bed_details/{hostel_id}/')
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


def room_list_view(request,pk):
    hostel_details=hostel_details_model.objects.get(hostel_id=pk)
    room_details=rooms_details_model.objects.filter(hostel_id_id=pk)
    bed_details=bed_details_model.objects.all()
    return render(request=request,template_name='room_list.html',context={'hostel_details':hostel_details,'room_details':room_details,'bed_details':bed_details})



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


def owner_main_view(request):
    return render(request=request,template_name='owner_main.html')



def my_hostel_details(request):
    res=hostel_details_model.objects.filter(owner_id=request.user.id)
    return render(request,template_name='myhostel.html',context={'hostel_details':res})