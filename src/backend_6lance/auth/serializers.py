from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)

class SignupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    surname = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)
    repassword = serializers.CharField(max_length=200)

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()