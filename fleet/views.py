from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Vehicle
from .serializers import VehicleSerializer

class VehicleListApiView(APIView):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        
        return Response(serializer.data)
    

    def post(self, request):
        serializer = VehicleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
class VehicleItemApiView(APIView):
    def get(self, request, id):
        vehicle = Vehicle.objects.filter(id=id).first()
        
        if not vehicle:
            return Response({'error':'vehicle not found!'}, status=404)
        
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

    def put(self, request, id):
        vehicle = Vehicle.objects.filter(id=id).first()

        if not vehicle:
            return Response({'error': 'vehicle not found!'}, status=404)

        serializer = VehicleSerializer(vehicle, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def patch(self, request, id):
        vehicle = Vehicle.objects.filter(id=id).first()

        if not vehicle:
            return Response({'error': 'vehicle not found!'}, status=404)

        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        vehicle = Vehicle.objects.filter(id=id).first()
        
        if not vehicle:
            return Response({'error':'vehicle not found!'}, status=404)
        
        vehicle.delete()
        return Response(status=204)
