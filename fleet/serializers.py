from rest_framework import serializers

from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicle
        fields = [
            'id',
            'name',
            'external_id',
            'status',
            'latitude',
            'longitude',
            'speed',
            'heading',
            'last_seen_at',
            'created_at',
            'updated_at'
        ]
        
    def get_latitude(self, obj):
        return obj.current_position.y
    
    def get_longitude(self, obj):
        return obj.current_position.x