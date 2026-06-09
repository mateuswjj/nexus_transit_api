from django.urls import path
from .views import VehicleListApiView

urlpatterns = [
    path("vehicles/", VehicleListApiView.as_view(), name="vehicle-list"),
]