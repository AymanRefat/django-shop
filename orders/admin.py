from django.contrib import admin
from .models import Order 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "status", "product", "amount"]
    search_fields = ["customer", "status", "product"]
    readonly_fields = ["created_time", "last_updated_time"]
