from django.core.mail import send_mail
from django.conf import settings
import requests
import os
from dotenv import load_dotenv
import logging
from rest_framework import status
from rest_framework.response import Response
# Create your views here.
logger = logging.getLogger("main")

load_dotenv()

url = "https://api.ng.termii.com/api/sms/send"

def send_email_otp(email, otp):
    # print(otp, 'from mail')
    try:
        send_mail(
        "Starletter e-mail verification",
        f"Dear user, your email verification code is {otp}",
        settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.info(f"Email Code error: {e}")
        return False
   
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
    
    # print(response)
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200 or response.status_code == 201:
            return True
        else:
            r = response.json()
            logger.info(f"Phone Number Code: {r}")
            return False
    except Exception as e:
        logger.info(f"Phone Number Code: {e}")
        return False
   
