from django import forms
from django.contrib.auth.hashers import make_password
from Customer.models import customer_register
from django.contrib.auth.models import User
from Customer.validators import clean_enter_new_password
import re

#customer registration page start
class cust_form(forms.ModelForm):
    repassword=forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        res=self.cleaned_data['username']
        temp=User.objects.all().values_list('username')
        if (res,) not in temp:
            raise forms.ValidationError('User not Found')


    class Meta:
        model=customer_register
        fields=['username','first_name','last_name','email','c_contact','c_dob','c_aadhaar','password','c_image','c_address']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not(username[0].isupper()):
            raise forms.ValidationError('username should start with uppercase character')
        if len(username)<3:
            raise forms.ValidationError('username should not be less than 3 characters')
        if len(username)>20:
            raise forms.ValidationError('username should not be greater than 20 characters')
        return username
    
    def clean_c_contact(self):
        cntno = self.cleaned_data['c_contact']
        if len(str(cntno))!=10:
            raise forms.ValidationError('phoneno must be 10 numbers')
        if str(cntno)[0] not in '9876':
            raise forms.ValidationError('phoneno should start with 9,8,7,6') 
        return cntno
    
    def clean_password(self):
        pswrd=self.cleaned_data['password']
        if len(pswrd)<3:
            raise forms.ValidationError('password should not be less than 3 characters')
        if len(pswrd)>20:
            raise forms.ValidationError('password should not be greater than 20 characters')
        if not(pswrd[0].isupper()):
            raise forms.ValidationError('password should start with uppercase character')
        if len(re.findall('[0-9]',pswrd))==0:
            raise forms.ValidationError('password must contain atleast one character')
        if len(re.findall('[^0-9a-zA-Z]',pswrd))==0:
            raise forms.ValidationError('password must contain atleast one special character')
        return pswrd
    
    def clean_repassword(self):
        pswrd=self.cleaned_data['repassword']
        if len(pswrd)<3:
            raise forms.ValidationError('repassword should not be less than 3 characters')
        if len(pswrd)>20:
            raise forms.ValidationError('repassword should not be greater than 20 characters')
        if not(pswrd[0].isupper()):
            raise forms.ValidationError('repassword should start with uppercase character')
        if len(re.findall('[0-9]',pswrd))==0:
            raise forms.ValidationError('repassword must contain atleast one character')
        if len(re.findall('[^0-9a-zA-Z]',pswrd))==0:
            raise forms.ValidationError('repassword must contain atleast one special character')
        if self.cleaned_data['password']!=pswrd:
            raise forms.ValidationError('password and repassword should be same')
        return pswrd
        
    def clean_c_aadhaar(self):
        aadhar=self.cleaned_data['c_aadhaar']
        if len(str(aadhar))!=12:
            raise forms.ValidationError('aadhar should contain 12 numbers')
        return aadhar
    
    def save(self,commit=True):
        user=super().save(commit=False)
        if self.cleaned_data['password']==self.cleaned_data['repassword']:
            user.password=make_password(self.cleaned_data['password'])
            if commit:
                user.save()
            return user
#customer registration page end


#owner loginpage start
class customer_login(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not(username[0].isupper()):
            raise forms.ValidationError('username should start with uppercase character')
        if len(username)<3:
            raise forms.ValidationError('username should not be less than 3 characters')
        if len(username)>20:
            raise forms.ValidationError('username should not be greater than 20 characters')
        return username    

    def clean_Password(self):
        pswrd=self.cleaned_data['password']
        if len(pswrd)<3:
            raise forms.ValidationError('password should not be less than 3 characters')
        if len(pswrd)>20:
            raise forms.ValidationError('password should not be greater than 20 characters')
        if not(pswrd[0].isupper()):
            raise forms.ValidationError('password should start with uppercase character')
        if len(re.findall('[0-9]',pswrd))==0:
            raise forms.ValidationError('password must contain atleast one character')
        if len(re.findall('[^0-9a-zA-Z]',pswrd))==0:
            raise forms.ValidationError('password must contain atleast one special character')
        return pswrd 
#owner loginpage end 



class changepswrd_form(forms.Form):
    enter_new_password=forms.CharField(widget=forms.PasswordInput,validators=[clean_enter_new_password,])
    reenter_new_password=forms.CharField(widget=forms.PasswordInput)

    def clean_reenter_new_password(self):
            print("how")
            pswrd=self.cleaned_data['reenter_new_password']
            if len(pswrd)<3:
                raise forms.ValidationError('repassword should not be less than 3 characters')
            if len(pswrd)>20:
                raise forms.ValidationError('repassword should not be greater than 20 characters')
            if not(pswrd[0].isupper()):
                raise forms.ValidationError('repassword should start with uppercase character')
            if len(re.findall('[0-9]',pswrd))==0:
                raise forms.ValidationError('repassword must contain atleast one character')
            if len(re.findall('[^0-9a-zA-Z]',pswrd))==0:
                raise forms.ValidationError('repassword must contain atleast one special character')
            if self.cleaned_data['enter_new_password']!=pswrd:
                raise forms.ValidationError('password and repassword should be same')
            return pswrd
    

