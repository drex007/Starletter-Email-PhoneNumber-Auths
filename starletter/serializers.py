from rest_framework import serializers
from .models import (PhoneStorage, EmailStorage)

class GenerateEmailOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailStorage
        fields = "__all__"

class GeneratePhoneNumberOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneStorage
        fields = "__all__"