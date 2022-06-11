from django.contrib import admin
from .models import Product, ProductImage, Category, ProductCategories , Flag


admin.site.register(Flag)
admin.site.register(ProductCategories)
admin.site.register(ProductImage)
class ProductImageAdmin(admin.TabularInline):
	model = ProductImage
	extra = 1





@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = [
		"name",
		"id",
		"inventory",
		"price",
	]
	filter_vertical = ["categories"]
	search_fields = ["id", "name", "price"]
	inlines = [ProductImageAdmin]
	readonly_fields = ["created_time", "last_updated_time"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ["name", "id"]

