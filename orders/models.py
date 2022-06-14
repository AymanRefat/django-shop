from __future__ import annotations
from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product 
from django.urls import reverse
User = get_user_model()
from django.utils.translation import gettext_lazy 


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        Paid = "P", gettext_lazy("Paid")
        Shipping = "S", gettext_lazy("Shipping")
        Done = "D", gettext_lazy("Done")

    id = models.AutoField(primary_key=True)
    customer: User = models.ForeignKey(User, on_delete=models.CASCADE)
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status: OrderStatus = models.CharField(
        max_length=2, choices=OrderStatus.choices, default=OrderStatus.Paid
    )

    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        status = Order.OrderStatus(self.status)
        return f"{self.product.name}{self.customer.username}-{status.label}"

    @property
    def total_price(self) -> float:
        return float(self.amount * self.product.price)

    def get_absolute_url(self) -> str:
        return reverse("get_order", kwargs={"pk": self.id})


    def edit(self) ->bool:
        """return if the order can be deleted or Edited """
        return True if self.status == Order.OrderStatus.Paid else False