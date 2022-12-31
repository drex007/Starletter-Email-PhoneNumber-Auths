from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .models import (PhoneStorage, EmailStorage)
from .otp_generator import generate_otp
from rest_framework import status
from rest_framework.response import Response
from .serializers import (GenerateEmailOtpSerializer, GeneratePhoneNumberOtpSerializer)
from .auth_messaging import send_email_otp,send_mobile_otp
from django.http import HttpResponse
from django.shortcuts import render

class GenerateEmailOtp(APIView):
    serializer_class = GenerateEmailOtpSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            
            instance=EmailStorage.objects.get(email=data['email'])
            otp = generate_otp()
            instance.otp = otp
            instance.save()
            send_email_otp(data["email"],otp )
            return Response(data={"message": "verification code has been sent to this already existing email"}, status=status.HTTP_201_CREATED)   
        except EmailStorage.DoesNotExist:
            inputs = {
                    "email": data['email'],
                    "otp": generate_otp()
                }
            serializer = self.serializer_class(data = inputs)
            if serializer.is_valid():
                serializer.save()
                send_email_otp(data["email"], inputs["otp"])
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        
email_otp = GenerateEmailOtp.as_view()

class VerifyEmailOtp(APIView):
    def post(self, request):
        data = request.data
        try:
            instance = EmailStorage.objects.get(email=data["email"])
            if instance.otp == data["otp"]:
                return Response(data={"message": "email is verified"}, status=status.HTTP_200_OK)
            return Response(data={"message": "You entered a wrong verification code"} , status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"message": "Error occured while verifying email"} , status=status.HTTP_400_BAD_REQUEST)
        

verify_email_otp = VerifyEmailOtp.as_view()



class GeneratePhoneNumberOtp(APIView):
    serializer_class = GeneratePhoneNumberOtpSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            instance=PhoneStorage.objects.get(phonenumber=data['phonenumber'])
            otp = generate_otp()
            instance.otp = otp
            instance.save()
            send_mobile_otp(data["phonenumber"], otp)
            return Response(data={"message": "verification code has been sent to this already phonenumber"}, status=status.HTTP_201_CREATED)   
        except PhoneStorage.DoesNotExist:
            inputs = {
                    "phonenumber": data['phonenumber'],
                    "otp": generate_otp()
                }
            serializer = self.serializer_class(data = inputs)
            if serializer.is_valid():
                serializer.save()
                send_mobile_otp(data["phonenumber"], inputs["otp"])
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        
mobile_otp = GeneratePhoneNumberOtp.as_view()






# Create your views here.
def index(request):
    return render(request,"starletter/index.html",{})