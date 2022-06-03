from django.forms import  ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.conf import settings
from django.views.generic.base import TemplateView
from .forms import NewUserForm
from django.views.generic.edit import FormView


class LogoutRequired(UserPassesTestMixin, View):
    permission_denied_message = "You have to Logout to see this page"

    def test_func(self) -> bool:
        return not self.request.user.is_authenticated


class UsersLoginView(LogoutRequired, LoginView):
    """View if the User Logout Only"""

    template_name = "users/login.html"


class UserLogoutView(LoginRequiredMixin, LogoutView):
    """View if the User Login Only"""

    template_name = "users/logout.html"
    login_url = settings.LOGIN_URL


class UserRegisterView(LogoutRequired, FormView, TemplateView):
    template_name = "users/register.html"
    form_class = NewUserForm
    context_object_name = "form"
    success_url = "login"

    def form_valid(self, form: ModelForm):
        form.save()
        return redirect(self.success_url)

    # TODO handel this in better way
    def form_invalid(self, form):
        return HttpResponse("bad Some thing happen ")
