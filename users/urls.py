from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    UserAccountDetailView,
    UserChangePassword,
    UserLogoutView,
    UserRegisterView,
    UsersLoginView,
)

# TODO Create Custom Reset Password views
# TODO Write the User Reset Password Templates
urlpatterns = [
    path("login/", UsersLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("<str:username>/", UserAccountDetailView.as_view(), name="account"),
    path(
        "<str:username>/password/change/",
        UserChangePassword.as_view(),
        name="password-change",
    ),
		# password_reset_confirm
    path(
        "password/reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password-reset.html"),
        name="password_reset",
    ),
    path(
        "password/reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password-reset-done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password-reset-change.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password-complete.html"
        ),
        name="password_reset_complet",
    ),
]
