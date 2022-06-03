from django.shortcuts import render 
from django.views import View
from django.views.generic import (
    DetailView,FormView
)
from .models import  Product
from .forms import ProductSearchForm


class ProductDetailView(DetailView):
    """See the All Details for the Product and User can Create Order from it"""


    model = Product
    template_name = "products/product.html"


class SearchProducts(View):
    template_name = "products/search.html"
    form_class = ProductSearchForm
    context_object_name = "form"

    # How to render the Form without Search when the form object is Empty 
    def get(self,request):
        """Render the Page Normal , If search Add the Objects to the Page"""
        form = self.form_class(request.GET or None)

        qs = None 
        if request.GET : 
            if form.is_valid():
                qs = form.search()
        
        return render(request,self.template_name,{'form':form,"products":qs })

