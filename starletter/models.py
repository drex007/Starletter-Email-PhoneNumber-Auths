from django.db import models

# Create your models here.


class EmailStorage(models.Model):
    email = models.CharField(blank=True, null=True, max_length=100)
    otp = models.CharField(blank=True, null=True, max_length=100)
    date_created = models.DateField(auto_now=True)
    
    
    def __str__(self) -> str:
        return f"{self.email}  :: {self.otp}"
    


class PhoneStorage(models.Model):
    phonenumber = models.CharField(blank=True, null=True, max_length=100)
    otp = models.CharField(blank=True, null=True, max_length=100)
    date_created = models.DateField(auto_now=True)
    
    
    def __str__(self) -> str:
        return f"{self.phonenumber}  :: {self.otp}"
    