from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import ListView, UpdateView, FormView
from django.http import HttpResponse
from .models import Order
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from typing import Optional
from django.forms.models import modelform_factory
from django.forms import NumberInput
from django.conf import settings
from products.models import Product
from .forms import CreateOrderForm


class GetOrders(LoginRequiredMixin, ListView):
    """Show the Users Orders in Table"""

    login_url = settings.LOGIN_URL

    template_name = "orders/orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by(
            "-created_time"
        )

    def post(self, request):
        order_id = request.POST.get("order_id")
        order: Order = Order.objects.get(id=order_id)
        order.delete()
        messages.success(request, "Order Deleted Successfully!")
        return self.get(request)


class CreateOrder(FormView, LoginRequiredMixin):
    context_object_name = "form"
    success_url = reverse_lazy("orders:orders")
    login_url = settings.LOGIN_URL

    template_name = "orders/create_order.html"
    form_class = CreateOrderForm

    def form_valid(self, form):
        """If the Form is Valid then Create the Order"""
        form.save(self.request.user)
        messages.success(self.request, "Order Created Successfully!")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """If the Form is Invalid then Show the Form Again"""
        messages.warning(self.request, "Order Creation Failed!")
        return self.render_to_response(self.get_context_data(form=form))



    # BUG -  if the user is not logged in and remove the product_id in url then it will NOT redirect to the login page
    def get_initial(self):
        """Get the Initial Data for the Form"""
        product_id = self.request.GET.get("product_id",None)
        if product_id is not None : 
            qs = Product.objects.filter(id=int(product_id))
            if qs.exists():
                return {"product": qs.first()}
        return super(FormView, self).get_initial()





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
