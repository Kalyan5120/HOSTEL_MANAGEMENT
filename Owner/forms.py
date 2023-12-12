from django import forms
from django.contrib.auth.hashers import make_password
from Owner.models import Owner_registration_model
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

