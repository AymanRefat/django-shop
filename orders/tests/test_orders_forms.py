from django.test import TestCase
from orders import forms 
from orders import models as m 
from products import models as p_models
from django.contrib.auth import get_user_model

User = get_user_model()

class TestOrdersForms(TestCase):

  def setUp(self) -> None:
    self.form_class = forms.CreateOrderForm
    self.user = User(username="test", password="ayman10M")
    self.product = p_models.Product(name="Test Product", description="Test Description", price=10,inventory=100)
    self.order = m.Order(product=self.product, amount=10)
    self.product.save()
    self.user.save()


  def test_return_value_from_CreateOrderForm_save_with_false(self):
    form = self.form_class(instance=self.order)
    result = form.save(self.user,False)
    self.assertIsInstance(result,m.Order)


  def test_return_value_from_CreateOrderForm_save_with_true(self):
    form = self.form_class(instance=self.order)
    result = form.save(self.user,True)
    self.assertIsInstance(result,m.Order)