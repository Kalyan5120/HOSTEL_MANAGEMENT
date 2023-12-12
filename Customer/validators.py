from django import forms
import re
def clean_enter_new_password(newpswrd):
        if len(newpswrd)<3:
            raise forms.ValidationError('password should not be less than 3 characters')
        if len(newpswrd)>20:
            raise forms.ValidationError('password should not be greater than 20 characters')
        if not(newpswrd[0].isupper()):
            raise forms.ValidationError('password should start with uppercase character')
        if len(re.findall('[0-9]',newpswrd))==0:
            raise forms.ValidationError('password must contain atleast one character')
        if len(re.findall('[^0-9a-zA-Z]',newpswrd))==0:
            raise forms.ValidationError('password must contain atleast one special character')
        return newpswrd