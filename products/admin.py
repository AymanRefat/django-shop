from django.contrib import admin
from .models import Product, ProductImage, ProductLabels, Label, Category, ProductCategories


admin.site.register(ProductCategories)
admin.site.register(ProductLabels)
admin.site.register(ProductImage)
class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "id",
        "inventory",
        "price",
    ]
    search_fields = ["id", "name", "price"]
    inlines = [ProductImageAdmin]
    readonly_fields = ["created_time", "last_updated_time"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]

