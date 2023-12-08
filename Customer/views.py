from django.shortcuts import render,redirect
from Customer.models import customer_register
from Customer.forms import cust_form,customer_login
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def customer_registration_view(request):
    form=cust_form()
    if request.method=='POST':
        form=cust_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    return render(request=request,template_name='customer_register.html',context={'form':form})



def customer_view(request):
    form=customer_login()
    if request.method=='POST':
        form=customer_login(request.POST)
        if form.is_valid():
            user=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
        if user:
            login(request,user)
            return redirect('/home')
    return render(request=request,template_name='customer_login.html',context={'form':form})


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponse('data is stored')


@login_required(login_url='/login')
def home_view(request):
    return render(request=request,template_name='home.html')


def customer_list(request):
    form=customer_register.objects.all()
    return render(request=request,template_name='customer_list.html',context={'form':form})