from django.contrib import admin

# Register your models here.
from .models import PhoneStorage, EmailStorage


admin.site.register([PhoneStorage, EmailStorage])
