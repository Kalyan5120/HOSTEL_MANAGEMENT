from django.shortcuts import render,redirect
from Owner.forms import Owner_login,Owner_registration_form
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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

