from django.db import models
from django.contrib.gis.db import models

class VehicleStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    MAINTENANCE = "maintenance", "Maintenance"
class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    plate = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=25,
        choices=VehicleStatus.choices,
        default=VehicleStatus.ACTIVE
    )
    
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)
    
    external_id = models.CharField(max_length=100, unique=True)
    speed = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    current_position = models.PointField(srid=4326, null=True, blank=True)
    heading = models.CharField(max_length=255, null=True, blank=True)
    last_seen_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    
