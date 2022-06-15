from django.urls import path
from .views import UsersLoginView, UserLogoutView, UserRegisterView, UserChangePassword
from django.contrib.auth import views as auth_views

app_name = 'users'
# TODO Create Custom Reset Password views
# TODO Write the User Reset Password Templates 
urlpatterns = [
    path("login/", UsersLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("change-password/", UserChangePassword.as_view(), name="change-password"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password-reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password-reset-done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password-reset-change.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password-complete.html"
        ),
        name="password_reset_complet",
    ),
]
