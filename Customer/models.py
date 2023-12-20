from django.db import models


# Create your models here.


class customer_book(models.Model):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    c_email=models.EmailField(unique=True)
    c_contact=models.PositiveBigIntegerField(unique=True)
    c_dob=models.DateField()
    c_address_proof=models.FileField()
    c_aadhaar=models.PositiveBigIntegerField(unique=True)
    c_image=models.ImageField()
    c_address=models.CharField(max_length=100)
    Duration_of_staying=models.PositiveBigIntegerField(default=1)
    hostel_id=models.PositiveBigIntegerField()
    room_id=models.PositiveIntegerField()
    bed_id=models.PositiveIntegerField()
    approved=models.BooleanField()
    service_agreement=models.FileField(null=True)


