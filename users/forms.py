from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, get_user_model, login
from django.core.mail import send_mail
from django.contrib.auth import authenticate, get_user_model
from .models import Address

User = get_user_model()


class NewUserForm(UserCreationForm):
		class Meta:
				model = User
				fields = ("username",'email' ,  "password1", "password2")


class UserChangePasswordForm(forms.Form):
		old_password = forms.CharField(widget=forms.PasswordInput)
		new_password = forms.CharField(widget=forms.PasswordInput)

		def change_password(self, user):
				if self.is_valid():
						old_password = self.cleaned_data.get("old_password")
						new_password = self.cleaned_data.get("new_password")
						user = authenticate(username=user.username, password=old_password)
						if user:
								user.set_password(new_password)
								user.save()
								print(user.__dict__)
								return user
						else:
								raise forms.ValidationError("Old Password is Incorrect")



