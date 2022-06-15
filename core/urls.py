from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.HomePage.as_view(),name='home'),
    path("products/", include("products.urls")),
    path("orders/", include("orders.urls")),
    path("", include("users.urls"))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
