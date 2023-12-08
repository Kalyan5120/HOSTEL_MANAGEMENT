from django.contrib import admin
from Customer.models import customer_register

# Register your models here.
class customer_registration_admin(admin.ModelAdmin):
    list_display=['username','first_name','last_name','email','c_contact','c_dob','c_aadhaar','password','c_image','c_address',]


admin.site.register(customer_register,customer_registration_admin)