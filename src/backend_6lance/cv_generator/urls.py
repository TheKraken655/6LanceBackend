from django.urls import path
from .views import CvUserData

urlpatterns = [
    path('user_data/', CvUserData.as_view(), name="Logout"),
]