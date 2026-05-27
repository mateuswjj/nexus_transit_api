from django.apps import AppConfig

'''
The `fleet` app manages all vehicle-related models, serializers, views, and routes.
It represents the vehicles that will be tracked and displayed on the map.
'''

class FleetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fleet'
