from django.test import TestCase, Client
from django.urls import reverse
from orders import models as m
from django.contrib.auth import get_user_model
from products import models as p_models

User = get_user_model()


class TestOrderViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User(username="test", password="ayman10M")
        self.product = p_models.Product(
            name="Test Product", description="Test Description", price=10, inventory=100
        )
        self.order = m.Order(product=self.product, customer=self.user, amount=10)

        self.product.save()
        self.user.save()
        self.order.save()

        self.create_order_url = reverse("orders:create")
        self.orders_url = reverse("orders:orders")
        self.edit_order_url = reverse("orders:edit", kwargs={"pk": self.order.id})

    def check_redirect_chain(self ,chain: list):
        if chain:
            return chain[0][0]
        else:
            return None

    # TODO make the login view dynamic using urllib parser
    def test_get_orders_view_not_log_in(self):
        response = self.client.get(self.orders_url, follow=True)
        print(response.redirect_chain)
        self.assertEqual(
            self.check_redirect_chain(response.redirect_chain), f"/login/?next=/orders/","The View Doesn't Redirect to the Login Page"
        )

    def test_get_create_order_view_not_log_in(self):
        response = self.client.get(self.create_order_url, follow=True)
        self.assertEqual(
            self.check_redirect_chain(response.redirect_chain),
            "/login/?next=/orders/create/",
            "The View Doesn't Redirect to the Login Page"
        )

    def test_get_edit_order_view_not_log_in(self):
        response = self.client.get(self.edit_order_url, follow=True)
        self.assertEqual(
            self.check_redirect_chain(response.redirect_chain),
            f"/login/?next=/orders/{self.order.pk}/edit",
            "The View Doesn't Redirect to the Login Page"
        )
