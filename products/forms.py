from itertools import product
from django import forms
from .models import Product
from django.db.models import QuerySet, Q


class ProductSearchFormByName(forms.ModelForm):
	class Meta:
		model = Product
		fields = ("name",)
		widgets = {
			"name": forms.TextInput(
				attrs={
					"class": "form-control me-2",
					"placeholder": "Search",
					"aria-label": "Search",
				}
			)
		}
		labels = {"name": ""}

	def search(self) -> QuerySet:
		"""search The Objects by name and describtion
		- if there is no Match return None
		- Use the Name in Describtion Search , If there is No describtion provided 
		"""
		if self.is_valid():
			obj = self.save(False)
			qs:QuerySet = Product.objects.search(**obj.__dict__)
			return qs 



class ProductSearchForm(forms.ModelForm):
	min_price = forms.FloatField(required=False)
	max_price = forms.FloatField(required=False)
	class Meta:
		model = Product
		fields = ("name", "labels", "categories")

	def __init__(self,*args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["name"].required = False  
		self.fields["labels"].required = False 
		self.fields["categories"].required = False 

	def search(self) -> QuerySet:
		"""search The Objects by name and describtion
		- if there is no Match return None
		- Use the Name in Describtion Search , If there is No describtion provided 
		"""
		if self.is_valid():
			qs:QuerySet = Product.objects.search(**self.cleaned_data)
			return qs 