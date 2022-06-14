from django.test import TestCase
from products import models as m 
from string import ascii_lowercase , ascii_uppercase 
import random 
from django.db.models import Q 


class TestProductSearch(TestCase):


		model = m.Product
		objects = model.objects

		def setUp(self):
				"""setup 100 Object has name of Car and random Chars with 70 has car and 30 don't"""
				self.keyword_search = "car"
				self.objects_count = 100
				self.diff_count = 40
				self.price = 1000 
				self.price2 = 500 
				self.cat1 = m.Category.objects.create(name="Sport")
				self.cat2 = m.Category.objects.create(name="Fashion")
				self.lab1 = m.Category.objects.create(name="New")
				self.lab2 = m.Category.objects.create(name="High-Rated")
				
				for i in range(self.objects_count):
						name = self.keyword_search + "".join(
								random.choices(ascii_uppercase + ascii_lowercase, k=10)
						)
						if i < self.diff_count:
								self.cat = self.cat1
								self.lab = self.lab1

								description = (
										"".join(random.choices(ascii_uppercase + ascii_lowercase, k=100))
										+ self.keyword_search
								)
						else:
								self.cat = self.cat2
								self.lab = self.lab2
								description = "None"
								self.price = self.price2
						
						obj = self.model(
								name=name, description=description, price=self.price, inventory=100
						)
						obj.save()
						obj.categories.add(self.cat)

		def test_search_products_by_name(self):
				qs = self.model.search(name=self.keyword_search)
				self.assertEqual(
						qs.count(), self.objects_count, "Can't find all objects have keywordCount"
				)

		def test_search_products_by_description(self):
				qs = self.model.search(
						description=self.keyword_search
				)  # should Return diff_count	
				self.assertEqual(
						qs.count(),
						self.diff_count,
						"Can't find all objects have keywordCount OR find More than Should",
				)

		def test_search_query_set_vs_filter(self):
				qs = self.objects.filter(
						Q(name__icontains=self.keyword_search)
						| Q(description__icontains=self.keyword_search)
				)
				qs2 = self.model.search(name=self.keyword_search)
				self.assertEqual(
						qs.count(), qs2.count(), "Search Method Doesn't Work at Name Search "
				)

		def test_search_query_vs_filter_method_by_description(self):
				qs =self.objects.filter(Q(description__icontains=self.keyword_search))
				qs2 =self.model.search(description=self.keyword_search)
				self.assertEqual(
						qs.count(), qs2.count(), "Search Method Doesn't Work at Describtion Search "
				)


		def test_search_query_min_price(self):
			qs = self.model.search(min_price=0)
			qs2 = self.objects.filter(price__gte=0)
			self.assertEqual(qs.count(),qs2.count(), "search Function doesn't work well with min_price Very Low Number")
			
			qs1 = self.model.search(min_price=self.price2)
			qs2 = self.objects.filter(price__gte=self.price2)
			
			self.assertEqual(qs1.count(),qs2.count() , "search Function doesn't work well with min_price in start with the Least Number")
			
			
			
			qs1 = self.model.search(min_price=self.price2+100)
			qs2 = self.objects.filter(price__gte=self.price2+100)
			self.assertEqual(qs1.count(),qs2.count() , "search Function doesn't work well with min_price High Number ")
			

	
		def test_search_query_max_price(self):
			qs1 = self.model.search(max_price=self.price2)
			qs2 = self.objects.filter(price__lte=self.price2)

			self.assertEqual(qs1.count(),qs2.count() , "search Function doesn't work well with max_price in start with the Least Number")
			qs1 = self.model.search(max_price=self.price2+100)
			qs2 = self.objects.filter(price__lte=self.price2+100)
			self.assertEqual(qs1.count(),qs2.count() , "search Function doesn't work well with max_price High Number ")
			
			qs = self.model.search(max_price=0)
			qs2 = self.objects.filter(price__lte=0)
			self.assertEqual(qs.count(),qs2.count(), "search Function doesn't work well with max_price (0)")
			

		def test_search_query_min_max_price(self):
			qs1 = self.model.search(min_price=0 , max_price=self.price + 100)
			qs2 = self.objects.filter(price__gte=0 , price__lte=self.price + 100)
			self.assertEqual(qs1.count(),qs2.count(), "search Function doesn't work well with min max pramas")


		def test_search_query_categories_with_Category_Object(self):
			qs1 = self.model.search(category=self.cat1)
			qs2 = self.objects.filter(categories=self.cat1)
			self.assertEqual(qs1.count(),qs2.count(), "search Function doesn't work well with categories pramas")


		def test_search_query_categories_with_qs(self):
			qs = self.model.search(category=[self.cat1])
			qs1 = self.objects.filter(categories__in=[self.cat1])
			self.assertEqual(qs.count(),qs1.count(), "search Function doesn't work well with Iterable Values")


		def test_search_query_categories_with_name(self):
			qs1 = self.model.search(category=self.cat1.name)
			qs2 = self.objects.filter(categories__name=self.cat1.name)
			self.assertEqual(qs1.count(),qs2.count(), "search Function doesn't work well with Categories string Values")

		def test_search_query_categories_raise_error(self):
			with self.assertRaises(TypeError)as err:
				self.model.search(category=True)



class TestImageHandeling(TestCase):
	pass 