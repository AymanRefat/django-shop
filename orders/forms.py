from django import forms
from .models import Order 
from django.contrib.auth import get_user_model
User = get_user_model()

class CreateOrderForm(forms.ModelForm):

	class Meta:
		model = Order
		fields = ["amount", "product"]
		labels = {"amount": "", "product": ""}
		widgets = {"amount": forms.NumberInput(attrs={"placeholder": "Amount"})}

	def save(self,customer:User, commit: bool = False ) -> Order :
		"""Save the Order Locally to add to it the Customer then Save it to the Database if you want
			Note: it Returns the Order Object in the Two Cases"""
		order = super().save(commit=False)
		order.customer = customer
		if commit :
			order.save(True)
			return order 
		else:
			return order