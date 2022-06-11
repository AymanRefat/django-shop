from __future__ import annotations
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.storages import select_storage
from . import utils 
from django.db.models import Q 

User = get_user_model()

class Flag(models.Model):
	name=models.CharField(max_length=10, unique=True)
	def __str__(self):
		return self.name

	@classmethod
	def get_defalut_flag(self):
		flag , created =  self.objects.get_or_create(name="Success")
		return flag.id 

class Category(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(null=False, blank=False, max_length=20)
	flag = models.ForeignKey(Flag , null=True,on_delete=models.CASCADE , default=Flag.get_defalut_flag)

	def __str__(self) -> str:
		return self.name

class Product(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, null=False, blank=False)
	describtion = models.TextField()
	price = models.FloatField()
	inventory = models.PositiveIntegerField()
	created_time = models.DateTimeField(auto_now_add=True)
	last_updated_time = models.DateTimeField(auto_now=True)
	categories = models.ManyToManyField(
		Category, through="ProductCategories", through_fields=( "product","category")
	)




	@classmethod
	def search(self,**kwargs)-> models.QuerySet:
		allowed = [ "name", "describtion", "price" , "category","min_price","max_price"]
		params = utils.valid_params(**utils.allowed_params(allowed=allowed,d=kwargs))
		name = params.get("name", None)
		describtion = params.get("describtion", None)
		price =params.get("price", None)
		min_price = params.get("min_price", None)
		max_price = params.get("max_price", None)
		category = params.get("category", None)


		qs = self.objects.all()

		if name is not None :
			qs = self.objects.filter(Q(describtion__icontains=name) | Q(name__icontains=name))

		if describtion is not None :
			qs = self.objects.filter(describtion__icontains=describtion)
		
		if price is not None :
			qs = self.objects.filter(price=price)

		if min_price is not None :
			qs = self.objects.filter(price__gte=min_price)

		if max_price is not None :
			qs = self.objects.filter(price__lte=max_price)

		if category is not None :
			if isinstance(category,Category):
				qs = self.objects.filter(categories=category)
			elif isinstance(category,str):
				qs = self.objects.filter(categories__name=category)
			elif hasattr(category,'__iter__') and  isinstance(category[0],Category):
				qs = self.objects.filter(categories__in=category)
			else:
				raise TypeError("category must be a Category, List Or String of Categories")
		
		return qs

	def __str__(self) -> str:
		return self.name

	def get_absolute_url(self) -> str:
		return reverse("products:product", kwargs={"pk": self.pk})

	@property
	def photos(self):
		return ProductImage.objects.filter(product=self)

	@property
	def base_photo(self):
		photos = self.photos
		if photos:
			return photos.first().image




class ProductCategories(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)








# TODO how to make one base Photo and others is Normal Photos 
class ProductImage(models.Model):
	id = models.AutoField(primary_key=True)
	image = models.ImageField(storage=select_storage,upload_to=utils.genrate_image_name)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	# base = models.BooleanField(default=True)

	def __str__(self) -> str:
		return self.product.name

