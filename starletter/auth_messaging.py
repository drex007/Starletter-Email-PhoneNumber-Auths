from django.core.mail import send_mail
from django.conf import settings
import requests

url = "https://api.ng.termii.com/api/sms/send"

def send_email_otp(email, otp):
    print(otp, 'from mail')
    send_mail(
        "Starletter e-mail verification",
        f"Dear user, your email verification code is {otp}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

def send_mobile_otp(phone, otp):
    print(str("+234" + phone))
    print(settings.SMS_SK)
    payload = {
        # "to": str("+234" + phone[1:]),
        "to": str("+234" + phone),
        "from": "Starletter",
        "sms": f"Your phone number verification cide is {otp}",
        "type": "plain",
        "channel": "generic",
        "api_key": settings.SMS_SK,
    }

    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response)
    
    return response
   
