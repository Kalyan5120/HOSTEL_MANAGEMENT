from django.contrib import admin
from Owner.models import Owner_registration_model

# Register your models here.
class owner_registration_admin(admin.ModelAdmin):
    list_display=['username','first_name','last_name','email','contactno','gender','password']


admin.site.register(Owner_registration_model,owner_registration_admin)