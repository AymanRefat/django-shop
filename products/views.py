from django.shortcuts import render 
from django.views import View
from django.views.generic import (
    DetailView
)
from .models import  Product , ProductImage , Category , ProductCategories , Flag
from .forms import ProductSearchForm
from django.contrib import messages 
from django.views.generic import ListView
from django.http import Http404

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
        form = self.form_class(request.GET)
        qs = None 
        if request.GET : 
            if form.is_valid():
                qs = form.search()
            else:
                qs = Product.objects.all()
                messages.warning(request, "Please Enter a Valid Search")
        return render(request,self.template_name,{'form':form,"products":qs })


class CategoryView(ListView):
    model = Product
    template_name = "products/category.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(categories__name__iexact=self.category)

    def get(self, request, *args, **kwargs):
        self.category = self.kwargs.get("category")
        qs = Category.objects.filter(name__iexact=self.category)
        if not qs.exists() :
            raise Http404(f"Category ({self.category}) Doesn't Exist")
        return super().get(request, *args, **kwargs)