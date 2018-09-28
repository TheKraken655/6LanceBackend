# Create your views here.
import pyrebase
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, SignupSerializer, ChangePasswordSerializer
from django.contrib.auth import logout

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
        }, headers={'Access-control-Allow-Origin': '*'})
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                request.session['uid'] = user['idToken']
                db = firebase.database()
                a = auth.get_account_info(request.session['uid'])
                a = a['users']
                a = a[0]
                emailVerified = str(a['emailVerified'])
                userid = a['localId']
                data = db.child('users').child(userid).get().val()
                if emailVerified == 'True':
                    data['emailVerified'] = 1
                    data = db.child('users').child(userid).set(data)
                return Response(data, headers={'Access-control-Allow-Origin': '*'})
            except:
                return Response({'message': 'Wrong email or password'}, headers={'Access-control-Allow-Origin': '*'})

class LogOut(APIView):
    def get(self, request, format=None):
        try:
            request.session['uid']
            logout(request)
            return Response({'message': 'Logout successfully'}, headers={'Access-control-Allow-Origin': '*'})
        except:
            return Response({'message': 'You must be logged in first'}, headers={'Access-control-Allow-Origin': '*'})

class SignUp(APIView):
    def get(self, request, format=None):
        return Response({
            'name': 'FirstName',
            'surname': 'Surname',
            'email': 'email@email.com',
            'password': 'password123',
            'repassword': 'password123'
        }, headers={'Access-control-Allow-Origin': '*'})
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
                    request.session['uid'] = user['idToken']
                    # Get a reference to the database service
                    db = firebase.database()

                    # Get user id
                    userid = auth.get_account_info(request.session['uid'])
                    userid = userid['users']
                    userid = userid[0]
                    userid = userid['localId']

                    # Data to save
                    data = {
                        "name": name,
                        "surname": surname,
                        "email": email,
                        "emailVerified": 0
                    }

                    # Push data to firebase database
                    db.child("users").child(userid).set(data)
                    return Response(data , headers={'Access-control-Allow-Origin': '*'})
                except:
                    return Response({'message': "Invalid Form"}, headers={'Access-control-Allow-Origin': '*'})

            return Response({'message': 'Passwords do not match'}, headers={'Access-control-Allow-Origin': '*'})

class ChangePasword(APIView):
    def get(self, request, format=None):
        return Response({
            'email': 'email@email.com'
        }, headers={'Access-control-Allow-Origin': '*'})
    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                auth.send_password_reset_email(email)
                return Response({'message': 'Email Sent'}, headers={'Access-control-Allow-Origin': '*'})
            except:
                return Response({'message': "Couldn't send email"}, headers={'Access-control-Allow-Origin': '*'})

