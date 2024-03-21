from django.urls import path

from .views import CustomerCreateView, CustomerDetailView, CustomerListView

urlpatterns = [
    path("", CustomerListView.as_view(), name="customer-list"),
    path("create/", CustomerCreateView.as_view(), name="customer-create"),
    path("<int:pk>/", CustomerDetailView.as_view(), name="customer-detailed"),
]
