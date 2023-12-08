from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class customer_register(User):
    c_contact=models.PositiveBigIntegerField(unique=True)
    c_dob=models.DateField()
    c_aadhaar=models.PositiveBigIntegerField(unique=True)
    c_image=models.ImageField()
    c_address=models.CharField(max_length=100)