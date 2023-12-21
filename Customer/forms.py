from django import forms
from Customer.models import customer_book


class book_room_form(forms.ModelForm):
    class Meta:
        model=customer_book
        exclude=['approved', 'service_agreement','hostel_id','room_id','bed_id']

    

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not(first_name[0].isupper()):
            raise forms.ValidationError('first_name should start with uppercase character')
        if len(first_name)<3:
            raise forms.ValidationError('first_name should not be less than 3 characters')
        if len(first_name)>20:
            raise forms.ValidationError('first_name should not be greater than 20 characters')
        return first_name
    



    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not(last_name[0].isupper()):
            raise forms.ValidationError('last_name should start with uppercase character')
        if len(last_name)<3:
            raise forms.ValidationError('last_name should not be less than 3 characters')
        if len(last_name)>20:
            raise forms.ValidationError('last_name should not be greater than 20 characters')
        return last_name
    


    def clean_c_contact(self):
        cntno = self.cleaned_data['c_contact']
        if len(str(cntno))!=10:
            raise forms.ValidationError('phoneno must be 10 numbers')
        if str(cntno)[0] not in '9876':
            raise forms.ValidationError('phoneno should start with 9,8,7,6') 
        return cntno


    def clean_c_aadhaar(self):
        adhaar = self.cleaned_data['c_aadhaar']
        if len(str(adhaar))!=12:
            raise forms.ValidationError('aadhaar should contain 12 numbers')
        
        return adhaar