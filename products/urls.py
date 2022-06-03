from django.urls import path
from .views import ProductDetailView, SearchProducts



app_name = 'products'
urlpatterns = [
    path("<int:pk>/", ProductDetailView.as_view(), name="product"),
    # path("search/", SearchProducts.as_view(), name="search"),
]
