from django.urls import path
from .views import LogIn, SignUp, ChangePasword, LogOut

urlpatterns = [
    path('login/', LogIn.as_view(), name="Logout"),
    path('logout/', LogOut.as_view(), name="Login"),
    path('signup/', SignUp.as_view(), name="Signup"),
    path('changepassword/', ChangePasword.as_view(), name="Change Password"),
]