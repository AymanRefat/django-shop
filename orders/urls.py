from django.urls import path
from .views import (
    GetOrders,
    UpdateOrder,
    CreateOrder,
)
app_name = 'orders'
urlpatterns = [
    path("", GetOrders.as_view(), name="orders"),
    path("create/", CreateOrder.as_view(), name="create"),
    path("<int:pk>/edit", UpdateOrder.as_view(), name="edit"),
]
