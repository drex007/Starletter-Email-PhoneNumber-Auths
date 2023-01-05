from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("email_otp/",views.email_otp, name="email_otp"),
    path("verify_email_otp/", views.verify_email_otp, name="verify_email_otp"),
    path("mobile_otp/", views.mobile_otp, name="mobile_otp"),
    path("verify_mobile_otp/", views.verify_mobile_otp, name="verify_mobile_otp"),
     
     
   
]

