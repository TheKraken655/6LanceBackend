import pyrebase
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CvUserDataSerializer
# Create your views here.

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

class CvUserData(APIView):
    def get(self, request, format=None):
        try:
            request.session['uid']
            return Response({
                'name': 'FirstName',
                'surname': 'Surname',
                'email': 'email@email.com',
                'telephone': '+541132385678',
                'cuil': '20-42145327-3',
                'postal_code': 1125,
                'address': 'Delgado 977',
                'province': 'Buenos Aires',
                'birth_date': '1998-05-25',
                'dni': 42145327
            }, headers={'Access-control-Allow-Origin': '*'})
        except:
            return Response({'message': 'You must be logged in first'}, headers={'Access-control-Allow-Origin': '*'})
    
    def post(self, request, format=None):
        try:
 
            db = firebase.database()

            serializer = CvUserDataSerializer(data=request.data)
            if serializer.is_valid():
                userid = auth.get_account_info(request.session['uid'])
                userid = userid['users']
                userid = userid[0]
                userid = userid['localId']

                db.child("users").child(userid).child("cv_user_data").set(serializer.data)
                data = db.child('users').child(userid).get().val()
                
            return Response(data, headers={'Access-control-Allow-Origin': '*'})    
        except:
            return Response({'message': 'You must be logged in first'}, headers={'Access-control-Allow-Origin': '*'})
