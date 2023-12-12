from django.shortcuts import render,redirect
from Owner.forms import Owner_login,Owner_registration_form
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from Owner.models import Owner_registration_model
import re


def owner_registration_view(request):
    form=Owner_registration_form()
    if request.method=='POST':
        form=Owner_registration_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/Owner/o_login')
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
    return redirect('/Owner/o_login')


@login_required(login_url='/Owner/owner_login')
def owner_home_view(request):
    return render(request=request,template_name='home_page.html')


#forget password 

otp_confirm=None

# @login_required(login_url='/Customer/customer_login')
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
            return redirect('/Customer/customer_otp')
        else:
            messages.error(request,'email is incorrect')
    return render(request=request,template_name='forget_password.html')


def otp_confirm_view(request):
    if request.method=='POST':
        if str(otp_confirm)==str(request.POST['otp_confirm']):
            return redirect('/Customer/changepswrd')
        else:
            return redirect('/Customer/forgetpswrd')
    return render(request=request,template_name='enterotp.html')
    

def changepswrd_view(request):
    return render(request=request,template_name='changepswrd.html')




    