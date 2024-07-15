# core/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("customers/", include("customers.urls")),
    path("", include("products.urls")),
    path("orders/", include("orders.urls")),
    path("pdfs/", include("pdfs.urls")),
]
