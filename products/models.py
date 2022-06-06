from __future__ import annotations
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.storages import select_storage
from . import utils 



User = get_user_model()

class Flag(models.Model):
	name=models.CharField(max_length=10, unique=True ,primary_key=True)
	
	def __str__(self):
		return self.name


class Label(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(null=False, blank=False, max_length=20)
	flag = models.ForeignKey(Flag , on_delete=models.CASCADE ,to_field='name',default='success' )
	
	def __str__(self) -> str:
		return self.name


class Category(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(null=False, blank=False, max_length=20)
	flag = models.ForeignKey(Flag , on_delete=models.CASCADE ,to_field='name',default='success' )

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
	labels = models.ManyToManyField(
		Label, through="ProductLabels", through_fields=( "product","label")
	)
	categories = models.ManyToManyField(
		Category, through="ProductCategories", through_fields=( "product","category")
	)

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




class ProductLabels(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	label = models.ForeignKey(Label, on_delete=models.CASCADE)


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

