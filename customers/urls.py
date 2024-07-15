from django.urls import path

# from .views_old import CustomerCreateView, CustomerDetailView, CustomerListView
from .views import CustomerListCreateView, CustomerRetrieveUpdateDestroyView

urlpatterns = [
    # path("", CustomerListView.as_view(), name="customer-list"),
    # path("create/", CustomerCreateView.as_view(), name="customer-create"),
    # path("<int:pk>/", CustomerDetailView.as_view(), name="customer-detailed"),
    path("", CustomerListCreateView.as_view(), name="customer-list-create"),
    path("<int:pk>/", CustomerRetrieveUpdateDestroyView.as_view(), name="customer-detail"),
]
