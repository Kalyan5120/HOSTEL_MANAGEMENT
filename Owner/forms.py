from typing import Any
from django import forms
from Owner.models import *
from django.contrib.auth.hashers import make_password
from Owner.models import Owner_registration_model,hostel_details_model,occupied_details_model,gallery_model,comments_model,rooms_details_model,bed_details_model
from Owner.validators import clean_enter_new_password
import re

# owner registration_admin start
class Owner_registration_form(forms.ModelForm):
    class Meta:
        model=Owner_registration_model
        fields=['username','first_name','last_name','email','contactno','gender','password','repassword'] 

    def clean_username(self):
        username = self.cleaned_data['username']
        if not(username[0].isupper()):
            raise forms.ValidationError('username should start with uppercase character')
        if len(username)<3:
            raise forms.ValidationError('username should not be less than 3 characters')
        if len(username)>20:
            raise forms.ValidationError('username should not be greater than 20 characters')
        return username
    
    def clean_contactno(self):
        cntno = self.cleaned_data['contactno']
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
    
    
    def save(self,commit=True):
        user=super().save(commit=False)
        if self.cleaned_data['password']==self.cleaned_data['repassword']:
            user.password=make_password(self.cleaned_data['password'])
            if commit:
                user.save()
            return user
        
#owner registration_admin end   

#owner loginpage start
class Owner_login(forms.Form):
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

#changepswrd

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


class hostel_details_form(forms.ModelForm):
    class Meta:
        model=hostel_details_model
        fields='__all__'

    def clean_phoneno(self):
        phoneno = self.cleaned_data['owner_phone_no']
        if len(str(phoneno))!=10:
            raise forms.ValidationError('phoneno must be 10 numbers')
        if str(phoneno)[0] not in '9876':
            raise forms.ValidationError('phoneno should start with 9,8,7,6') 
        return phoneno
    

class gallery_form(forms.ModelForm):
    class Meta:
        model=gallery_model
        fields='__all__'

class comments_form(forms.ModelForm):
    class Meta:
        model=comments_model
        fields='__all__'

class room_details_form(forms.ModelForm):
    class Meta:
        model=rooms_details_model
        fields='__all__'

    def clean_room_no(self):
        room=self.cleaned_data['room_no']
        if (room,)  in rooms_details_model.objects.filter(hostel_id=self.data['hostel_id']).values_list('room_no'):
            raise forms.ValidationError("room number already exist")
        return room


class bed_details_form(forms.ModelForm):
    class Meta:
        model=bed_details_model
        fields='__all__'

    def clean(self):
        room=self.cleaned_data['room_no'].room_no
        bed=self.cleaned_data['bed_no']
        res=rooms_details_model.objects.get(hostel_id=int(self.data['hid']),room_no=room)
        if int(bed)>int(res.num_of_beds):
            raise forms.ValidationError(f'Bed Number Should be below {int(res.num_of_beds)+1}')
        bed=self.cleaned_data['bed_no']
        if (bed,)  in bed_details_model.objects.filter(room_no_id=self.cleaned_data['room_no'].room_id).values_list('bed_no'):
            raise forms.ValidationError(f"Bed no {bed} already exist")


class occupied_details_form(forms.ModelForm):
    class Meta:
        model=occupied_details_model
        fields='__all__'

    def clean_phoneno(self):
        phoneno = self.cleaned_data['phone_no']
        if len(str(phoneno))!=10:
            raise forms.ValidationError('phoneno must be 10 numbers')
        if str(phoneno)[0] not in '9876':
            raise forms.ValidationError('phoneno should start with 9,8,7,6') 
        return phoneno
    
    def clean_age(self):
        age = self.cleaned_data['age']
        if len(str(age))<=15:
            raise forms.ValidationError('age must be 15 years')
        
    def clean_aadhar(self):
        aadhar = self.cleaned_data['aadhar']
        if len(str(aadhar))!=12:
            raise forms.ValidationError('aadhar no must contain 12 numbers')