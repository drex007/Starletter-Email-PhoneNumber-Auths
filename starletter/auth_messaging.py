from django.core.mail import send_mail
from django.conf import settings
import requests
import os
from dotenv import load_dotenv
load_dotenv()

url = "https://api.ng.termii.com/api/sms/send"

def send_email_otp(email, otp):
    # print(otp, 'from mail')
    send_mail(
        "Starletter e-mail verification",
        f"Dear user, your email verification code is {otp}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

def send_mobile_otp(phone, otp):
    send_phoneumber = f"+234{phone[1:]}" if phone[0] == "0" else f"+234{phone}"
    payload = {
      
        "to": send_phoneumber,
        "from": "Starletter",
        "sms": f"Your phone number verification code is {otp}",
        "type": "plain",
        "channel": "generic",
        "api_key": str(os.getenv("SMS_API")),
    }

    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return True
    return False
   
