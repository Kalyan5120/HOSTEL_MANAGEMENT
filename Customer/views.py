from django.shortcuts import render,redirect
from Customer.forms import cust_form,customer_login,changepswrd_form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import random
from django.conf import settings
from django.core.mail import send_mail
from Customer.models import customer_register
from django.contrib import messages
from django.contrib.auth.hashers import make_password



# Create your views here.
def customer_registration_view(request):
    form=cust_form()
    if request.method=='POST' and request.FILES:
        form=cust_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/Customer/customer_login')
    return render(request=request,template_name='customer_register.html',context={'form':form})



def customer_view(request):
    form=customer_login()
    if request.method=='POST':
        form=customer_login(request.POST)
        if form.is_valid():
            user=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
        if user:
            login(request,user)
            return redirect('/Customer/home')
        else:
            messages.error(request,'username or password is incorrect')
            return redirect('/Customer/customer_login')
    return render(request=request,template_name='customer_login.html',context={'form':form})

@login_required(login_url='/Customer/customer_login')
def customer_list(request):
    form=customer_register.objects.all()
    return render(request=request,template_name='customer_list.html',context={'form':form})
   

def p_details_view(request):   
    return render(request=request,template_name='p_details.html')

@login_required(login_url='/Customer/customer_login')
def logout_view(request):
    logout(request)
    return redirect('/Customer/customer_login')


@login_required(login_url='/Customer/customer_login')
def home_view(request):
    return render(request=request,template_name='home.html')

#forget password 

otp_confirm=None


def forgetpassword_view(request):
    res=customer_register.objects.all().values_list('email')    
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
            email_id=customer_register.objects.get(email=email)
            return redirect(f'/Customer/customer_otp/{email_id.id}/')
        else:
            messages.error(request,'email is incorrect')
    return render(request=request,template_name='forget_password.html')


def otp_confirm_view(request,pk):
    if request.method=='POST':
        if str(otp_confirm)==str(request.POST['otp_confirm']):
            return redirect(f'/Customer/changepswrd/{pk}/')
        else:
            return redirect('/Customer/forgetpswrd')
    return render(request=request,template_name='enterotp.html')
    

def changepswrd_view(request,pk):
    form=changepswrd_form()
    if request.method=='POST':
        res=customer_register.objects.get(id=pk)
        form=changepswrd_form(request.POST)
        print(form)
        if form.is_valid():
            print("bye")
            if form.cleaned_data['enter_new_password']==form.cleaned_data['reenter_new_password']:
                customer_register.objects.filter(id=pk).update(password=make_password(form.cleaned_data['enter_new_password']))
                return redirect('/Customer/customer_login')
    return render(request=request,template_name='changepswrd.html',context={'form':form})




    