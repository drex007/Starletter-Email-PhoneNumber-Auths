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
    #Added comments
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            
            instance=EmailStorage.objects.filter(email=data['email']).first()
            otp = generate_otp()
            instance.otp = otp
            instance.save()
            send_email_otp(data["email"],otp )
            return Response(data={"message": "verification code has been sent to this already existing email"}, status=status.HTTP_201_CREATED)   
        except (EmailStorage.DoesNotExist , AttributeError) as e:
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
            instance = EmailStorage.objects.filter(email=data["email"]).first()
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
        phone = data["phonenumber"][1:] if data["phonenumber"][0] == "0" else  data["phonenumber"]
        try:
            instance=PhoneStorage.objects.filter(phonenumber=phone).first()
            otp = generate_otp()
            instance.otp = otp
            instance.save()
            sms_status = send_mobile_otp(data["phonenumber"], otp)
            if sms_status:
                return Response(data={"message": "verification code has been sent to this already phonenumber"}, status=status.HTTP_201_CREATED) 
            return Response(data={"message": "An error occured while trying to send a verification code"}, status=status.HTTP_400_BAD_REQUEST)    
        except (PhoneStorage.DoesNotExist , AttributeError) as e:
            inputs = {
                    "phonenumber": phone,
                    "otp": generate_otp()
                }
            serializer = self.serializer_class(data = inputs)
            
            sms_status = send_mobile_otp(data["phonenumber"], inputs["otp"])
            if sms_status:
                if serializer.is_valid():
                    serializer.save()
            
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        
mobile_otp = GeneratePhoneNumberOtp.as_view()

class VerifyMobileOtp(APIView):
    def post(self, request):
        data = request.data
        phone = data["phonenumber"][1:] if data["phonenumber"][0] == "0" else  data["phonenumber"]
        try:
            instance = PhoneStorage.objects.filter(phonenumber=phone).first()
            if instance.otp == data["otp"]:
                return Response(data={"message": "Phone number is verified"}, status=status.HTTP_200_OK)
            return Response(data={"message": "You entered a wrong verification code"} , status=status.HTTP_400_BAD_REQUEST)
        except (PhoneStorage.DoesNotExist, AttributeError) as e:
            return Response(data={"message": "Error occured while verifying Phone number"} , status=status.HTTP_400_BAD_REQUEST)
        

verify_mobile_otp = VerifyMobileOtp.as_view()






# Create your views here.
def index(request):
    return render(request,"starletter/index.html",{})