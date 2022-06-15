from django.views.generic import ListView

from products.forms import ProductSearchFormByName
from products.models import Product


class HomePage(ListView):
		"""View all products we have now , The User can Click on Product to see more Details and Order it"""

		model = Product
		template_name = "home.html"
		context_object_name = "products"	
		search_form = ProductSearchFormByName
		



		def get_queryset(self):
				search_data = self.request.GET
				search_form = self.search_form(search_data)
				# this means there is Search Query 
				return search_form.search() or super().get_queryset()
			
	
		
		def get_context_data(self)->dict:
			context = super().get_context_data()
			context['search_form'] = self.search_form()
			return context