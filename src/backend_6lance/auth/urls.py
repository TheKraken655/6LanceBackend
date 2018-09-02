from django.urls import path
from .views import LogIn, SignUp, ChangePasword

urlpatterns = [
    path('login/', LogIn.as_view(), name="Login"),
    path('signup/', SignUp.as_view(), name="Signup"),
    path('changepassword/', ChangePasword.as_view(), name="Change Password"),
]