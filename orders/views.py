from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import (
		ListView,
		UpdateView,
)
from django.http import HttpResponse
from .models import Order
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from typing import Optional
from django.forms.models import modelform_factory
from django.forms import NumberInput
from django.conf import settings
from products.models import Product


class GetOrders(LoginRequiredMixin, ListView):
		"""Show the Users Orders in Table"""

		login_url = settings.LOGIN_URL

		template_name = "orders/orders.html"
		context_object_name = "orders"

		def get_queryset(self):
				return Order.objects.filter(customer=self.request.user)

		def post(self, request):
				order_id = request.POST.get("order_id")
				order: Order = Order.objects.get(id=order_id)
				order.delete()
				messages.success(request , "Order Deleted Successfully!")
				return redirect("orders:orders")


# TODO there is a better way
# TODO Put the Form in the Forms File
# This mustn't be here because he must create the order from The Product itself
class CreateOrder(LoginRequiredMixin, TemplateView):
		context_object_name = "form"
		fields = ["amount", "product"]
		labels = {"amount": "", "product": ""}
		widgets = {"amount": NumberInput(attrs={"placeholder": "Amount"})}
		success_url = reverse_lazy("orders:orders")
		login_url = settings.LOGIN_URL

		template_name = "orders/create_order.html"
		model = Order
		Form = modelform_factory(Order, fields=fields, labels=labels, widgets=widgets)

		def post(self, request):
				form = self.Form(request.POST)
				try:
						if form.is_valid():
								order = form.save(False)
								order.customer = request.user
								order.save()
								messages.success(request, "Order Created Successfully!")
								return redirect(self.success_url)
				except:
						return Http404("Some Thing Went Wrong")

		def form(self):
				if product_id := self.request.GET.get("product_id"):
						product = Product.objects.get(id=product_id)
						return self.Form(initial={"product": product})
				return self.Form()

		def get_context_data(self, **kwargs):
				context = super().get_context_data(**kwargs)
				context[self.context_object_name] = self.form()
				return context


class UpdateOrder(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
		"""Update Order"""

		login_url = settings.LOGIN_URL
		model = Order
		context_object_name = "form"
		fields = ["amount", "product"]
		success_url = reverse_lazy("orders:orders")
		template_name = "orders/update_order.html"

		def test_func(self) -> Optional[bool]:
				object: Order = self.get_object()
				return self.request.user == object.customer

		def form_valid(self, form) -> HttpResponse:
				messages.success(self.request, "Order Updated Successfully!")
				return super().form_valid(form)
