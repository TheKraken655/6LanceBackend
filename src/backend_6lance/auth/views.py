from django.shortcuts import render

# Create your views here.
import pyrebase
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, SignupSerializer, ChangePasswordSerializer

config = {
    'apiKey': "AIzaSyBWGSQtKAy5PxJ9cHQaYQzfTeuaHHfNaPM",
    'authDomain': "lance-4869f.firebaseapp.com",
    'databaseURL': "https://lance-4869f.firebaseio.com",
    'projectId': "lance-4869f",
    'storageBucket': "lance-4869f.appspot.com",
    'messagingSenderId': "840330781308"
  }

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

class LogIn(APIView):
    def get(self, request, format=None):
        return Response({
            'email': 'email@email.com',
            'password': 'password123'
        })
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                return Response(auth.get_account_info(user['idToken']))
            except:
                return Response({'message': 'Wrong email or password'})

class SignUp(APIView):
    def get(self, request, format=None):
        return Response({
            'name': 'FirstName',
            'surname': 'Surname',
            'email': 'email@email.com',
            'password': 'password123',
            'repassword': 'password123'
        })
    def post(self, request, format=None):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            surname = serializer.validated_data.get('surname')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            repassword = serializer.validated_data.get('repassword')
            
            if password == repassword:
                try:      
                    user = auth.create_user_with_email_and_password(email, password)
                    auth.send_email_verification(user['idToken'])
                    # Get a reference to the database service
                    db = firebase.database()

                    # data to save
                    data = {
                        "name": name,
                        "surname": surname,
                        "email": email,
                    }
                    results = db.child("users").push(data, user['idToken'])

                    return Response(auth.get_account_info(user['idToken']))
                except:
                    return Response({'message': "Invalid Form"})

            return Response({'message': 'Passwords do not match'})

class ChangePasword(APIView):
    def get(self, request, format=None):
        return Response({
            'email': 'email@email.com'
        })
    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                auth.send_password_reset_email(email)
                return Response({'message': 'Email Sent'})
            except:
                return Response({'message': "Couldn't send email"})

