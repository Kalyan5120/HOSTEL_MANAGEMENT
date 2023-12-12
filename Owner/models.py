from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Owner_registration_model(User):
    gender=models.CharField(max_length=10,choices=[['female','female'],['male','male']])
    contactno=models.PositiveBigIntegerField(unique=True)
    repassword=models.CharField(max_length=20)
    