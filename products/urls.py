from django.urls import path
from .views import ProductDetailView, SearchProducts, CategoryView



app_name = 'products'
urlpatterns = [
    path("<int:pk>/", ProductDetailView.as_view(), name="product"),
    path('search/',SearchProducts.as_view(),name='search'),
    path('<str:category>/',CategoryView.as_view(),name='category'),
]
