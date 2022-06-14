from django.test import TestCase 
from orders import models as m 
from django.contrib.auth import get_user_model
from products import models as p_models

User = get_user_model()



class TestOrdersModels(TestCase):

  def setUp(self) -> None:
    self.user = User(username="test", password="ayman10M")
    self.product = p_models.Product(name="Test Product", description="Test Description", price=10,inventory=100)
    self.order = m.Order(product=self.product, amount=10)
    self.product.save()
    self.user.save()


  def test_order_total_price(self):
    self.assertEqual(self.order.total_price,self.product.price*self.order.amount)
    
  def test_order_total_price_type(self):
    self.assertIsInstance(self.order.total_price,float)

