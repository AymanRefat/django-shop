from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login , authenticate , get_user_model
# from django.contrib.auth.models import User 

User = get_user_model()
# print(User)
class NewUserForm(UserCreationForm):

	class Meta:
		model = User
		fields = ("username",  "password1", "password2")


	# def login(self,request)->bool:
	# 	"""return True if Login the User"""
	# 	user = self.save(False)
	# 	print(user)
	# 	user.save()
	# 	auth_user = authenticate(request,username=user.username,password=user.password)
	# 	if auth_user:
	# 		login(request,auth_user)
	# 		return True
	# 	return False 

