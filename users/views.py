from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import ModelForm
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import  DetailView
from django.views.generic.edit import FormView


# Local Imports
from typing import Optional
from . import forms
from .forms import  UserChangePasswordForm

User = get_user_model()


class UsersLoginView(LoginView):
		"""View if the User Logout Only"""

		template_name = "users/login.html"
		success_url: Optional[str] = reverse_lazy("home")

		def get(self, request, *args, **kwargs):
				if request.user.is_authenticated:
						messages.warning(request, f"You are already Logged In as {request.user} ")
						return redirect("home")
				return super(LoginView, self).get(request, *args, **kwargs)

		def form_valid(self, form):
				"""If the Form is Valid then Login the User"""
				login(self.request, form.get_user())
				messages.success(
						self.request,
						f"You are Logged In as {form.cleaned_data['username']} Successfully",
				)
				return redirect(self.get_success_url())


class UserLogoutView(View):
		"""View if the User Login Only"""

		template_name = "users/logout.html"
		success_url = "home"

		def get(self, request):
				if not request.user.is_authenticated:
						messages.warning(request, f"You are already not Logged In")
						return redirect("users:login")
				elif request.user.is_authenticated:
						logout(request)
						messages.success(request, f"You are Logged Out Successfully")
						return redirect(self.success_url)


class UserRegisterView(FormView):
		template_name = "users/register.html"
		form_class = forms.NewUserForm
		context_object_name = "form"
		success_url = reverse_lazy("home")

		def get(self, request):
				if request.user.is_authenticated:
						messages.warning(request, f"You are already Logged In as {request.user} ")
						return redirect(self.success_url)
				return super().get(request)

		def form_valid(self, form: ModelForm):
				"""Login User after Register"""
				user = form.save()
				login(self.request, user)
				messages.success(
						self.request, "You have been Registered and loged in Successfully"
				)
				return redirect(self.success_url)

		def form_invalid(self, form):
				return self.get(self.request)


class UserChangePassword(LoginRequiredMixin, FormView):

		template_name = "users/change-password.html"
		success_url = reverse_lazy("home")
		form_class = UserChangePasswordForm

		def form_valid(self, form: UserChangePasswordForm):
				user = form.change_password(self.request.user)
				messages.success(self.request, "Password Changed Successfully")
				update_session_auth_hash(self.request, user)
				return redirect(self.success_url)

		def form_invalid(self, form):
				messages.error(self.request, "Please Enter Valid Password")
				return self.get(self.request)


class UserAccountDetailView(LoginRequiredMixin, DetailView):
		template_name = "users/account.html"
		model = User
		context_object_name = "user"

		def get_object(self, queryset=None):
				username = self.kwargs.get("username",None)
				if username is not None:
						return User.objects.get(username=username)
				else:
					Http404("Invalid User Name")