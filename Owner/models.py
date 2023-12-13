from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Owner_registration_model(User):
    gender=models.CharField(max_length=10,choices=[['Female','Female'],['Male','Male']])
    contactno=models.PositiveBigIntegerField(unique=True)
    repassword=models.CharField(max_length=20)



class hostel_details_model(models.Model):
    hostel_id=models.AutoField(primary_key=True)
    hostel_name=models.CharField(max_length=20,unique=True)
    address=models.TextField(max_length=100)
    GST=models.CharField(max_length=15,unique=True)
    license=models.CharField(max_length=20,unique=True)
    type_of_hostel=models.CharField(max_length=10,choices=[['Male','Male'],['Female','Female'],['Co_living','Co_living']])
    hostel_owner_name=models.CharField(max_length=30)
    owner_id=models.PositiveIntegerField()
    owner_phone_no=models.PositiveBigIntegerField(unique=True)
    owner_email=models.EmailField(unique=True)
    vaccancy=models.PositiveBigIntegerField()
    rating=models.DecimalField(max_digits=2,decimal_places=1)
    def __str__(self):
        return self.hostel_name

class gallery_model(models.Model):
    gallery_id=models.AutoField(primary_key=True)
    hostel_id=models.PositiveIntegerField()
    images=models.ImageField(upload_to='hostel/')

class comments_model(models.Model):
    comments_id=models.AutoField(primary_key=True)
    hostel_id=models.PositiveIntegerField()
    comments=models.TextField(max_length=100)

class rooms_details_model(models.Model):
    hostel_id=models.ForeignKey(hostel_details_model,on_delete=models.CASCADE)
    room_id=models.AutoField(primary_key=True)
    room_no=models.PositiveIntegerField()
    num_of_beds=models.PositiveIntegerField()
    def __str__(self):
        return str(self.room_no)


class bed_details_model(models.Model):
    bed_id=models.AutoField(primary_key=True)
    room_no=models.ForeignKey(rooms_details_model,on_delete=models.CASCADE)
    bed_no=models.CharField(choices=[['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6']],max_length=10)
    bed_cost=models.PositiveIntegerField()
    availability=models.BooleanField()
    def __str__(self):
        return str(self.bed_no)

class occupied_details_model(models.Model):
    occ_id=models.AutoField(primary_key=True)
    bed_id=models.ForeignKey(bed_details_model,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    phone_no=models.PositiveBigIntegerField()
    age=models.PositiveIntegerField()
    gender=models.CharField(max_length=10,choices=[['Male','Male'],['Female','Female'],['others','others']])
    email=models.EmailField(unique=True)
    aadhaar=models.PositiveBigIntegerField()
    image=models.ImageField(upload_to='profile/',null=True)
    def __str__(self):
        return self.name
