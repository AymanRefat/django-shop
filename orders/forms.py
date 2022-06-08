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

	def save(self,customer:User, commit: bool = ... ) -> Order | None:
		order = super().save(commit=False)
		order.customer = customer
		if commit :
			order.save(True)
		else:
			return order