from django.shortcuts import render,redirect
from Customer.forms import cust_form
from django.contrib.auth import authenticate
from django.http import HttpResponse

# Create your views here.
def customer_registration_view(request):
    form=cust_form()
    if request.method=='POST':
        form=cust_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('data is stored')
    return render(request=request,template_name='customer_register.html',context={'form':form})



def customer_login(request):
    form=cust_form()
    if request.method=='POST':
        form=cust_form(request.POST)
        if form.is_valid():
            user=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
        if user:
            login(request,user)
            return HttpResponse('data is stored')
        return render(request=request,template_name='customer_login.html',context={'form':form})