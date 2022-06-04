from django.urls import path
from .views import UsersLoginView, UserLogoutView,UserRegisterView

urlpatterns = [
    path("login/", UsersLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path('register/',UserRegisterView.as_view(),name="register")
]