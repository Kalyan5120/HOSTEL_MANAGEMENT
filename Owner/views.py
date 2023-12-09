from django.shortcuts import render,redirect
from Owner.forms import Owner_login
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_view(request):
    form=Owner_login()
    if request.method=='POST':
        form=Owner_login(request.POST)
        if form.is_valid():
            user=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
        if user:
            login(request,user)
            return redirect('/Owner/home')
    return render(request=request,template_name='owner_login.html')


@login_required(login_url='/Owner/owner_login')
def logout_view(request):
    logout(request)
    return redirect('/Owner/Owner_login')


@login_required(login_url='/Owner/owner_login')
def home_view(request):
    return render(request=request,template_name='home_page.html')