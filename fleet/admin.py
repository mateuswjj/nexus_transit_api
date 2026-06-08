from django.contrib.gis import admin
from django.contrib.gis.forms import OSMWidget

from .models import Vehicle


class VehicleMapWidget(OSMWidget):
    map_srid = 4326


@admin.register(Vehicle)
class VehicleAdmin(admin.GISModelAdmin):
    gis_widget = VehicleMapWidget
