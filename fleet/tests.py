from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Vehicle, VehicleStatus


class VehicleApiTests(APITestCase):
    def create_vehicle(self, **overrides):
        data = {
            'name': 'Vehicle 1',
            'plate': 'ABC1234',
            'external_id': 'veh-001',
            'is_active': True,
            'status': VehicleStatus.ACTIVE,
            'current_position': Point(-46.6333, -23.5505, srid=4326),
            'speed': '35.50',
            'heading': 'North',
            'last_seen_at': '2026-06-13T12:00:00Z',
        }
        data.update(overrides)
        return Vehicle.objects.create(**data)

    def test_list_vehicles_returns_all_vehicles(self):
        self.create_vehicle()
        self.create_vehicle(
            name='Vehicle 2',
            plate='DEF5678',
            external_id='veh-002',
        )

        response = self.client.get(reverse('vehicle-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_vehicle_creates_vehicle(self):
        payload = {
            'name': 'Vehicle 3',
            'plate': 'GHI9012',
            'external_id': 'veh-003',
            'is_active': True,
            'status': VehicleStatus.ACTIVE,
            'current_position': 'SRID=4326;POINT (-46.6333 -23.5505)',
            'speed': '42.25',
            'heading': 'East',
            'last_seen_at': '2026-06-13T12:10:00Z',
        }

        response = self.client.post(reverse('vehicle-list'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertEqual(response.data['plate'], payload['plate'])
        self.assertEqual(
            response.data['current_position'],
            payload['current_position'],
        )

    def test_get_vehicle_returns_vehicle_details(self):
        vehicle = self.create_vehicle()

        response = self.client.get(reverse('vehicle-item', args=[vehicle.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], vehicle.id)
        self.assertEqual(response.data['plate'], vehicle.plate)

    def test_get_vehicle_returns_404_when_vehicle_does_not_exist(self):
        response = self.client.get(reverse('vehicle-item', args=[999]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'vehicle not found!'})

    def test_put_vehicle_updates_all_fields(self):
        vehicle = self.create_vehicle()
        payload = {
            'name': 'Vehicle Updated',
            'plate': 'XYZ9999',
            'external_id': 'veh-999',
            'is_active': False,
            'status': VehicleStatus.MAINTENANCE,
            'current_position': 'SRID=4326;POINT (-46.6000 -23.5000)',
            'speed': '12.75',
            'heading': 'South',
            'last_seen_at': '2026-06-13T12:30:00Z',
        }

        response = self.client.put(reverse('vehicle-item', args=[vehicle.id]), payload, format='json')

        vehicle.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(vehicle.name, payload['name'])
        self.assertEqual(vehicle.plate, payload['plate'])
        self.assertEqual(vehicle.external_id, payload['external_id'])
        self.assertFalse(vehicle.is_active)
        self.assertEqual(vehicle.status, payload['status'])
        self.assertEqual(vehicle.current_position.x, -46.6)
        self.assertEqual(vehicle.current_position.y, -23.5)

    def test_patch_vehicle_updates_partial_fields(self):
        vehicle = self.create_vehicle()
        payload = {
            'status': VehicleStatus.INACTIVE,
            'heading': 'West',
        }

        response = self.client.patch(reverse('vehicle-item', args=[vehicle.id]), payload, format='json')

        vehicle.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(vehicle.status, payload['status'])
        self.assertEqual(vehicle.heading, payload['heading'])
        self.assertEqual(vehicle.name, 'Vehicle 1')

    def test_delete_vehicle_removes_vehicle(self):
        vehicle = self.create_vehicle()

        response = self.client.delete(reverse('vehicle-item', args=[vehicle.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vehicle.objects.filter(id=vehicle.id).exists())
