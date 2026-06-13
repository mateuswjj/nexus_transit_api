from django.urls import path
from .views import VehicleItemApiView, VehicleListApiView

urlpatterns = [
    path("vehicles/", VehicleListApiView.as_view(), name="vehicle-list"),
    path("vehicle/<int:id>", VehicleItemApiView.as_view(), name='vehicle-item')
]