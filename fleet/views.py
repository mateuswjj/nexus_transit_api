from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Vehicle
from .serializers import VehicleSerializer

class VehicleListApiView(APIView):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        
        return Response(serializer.data)