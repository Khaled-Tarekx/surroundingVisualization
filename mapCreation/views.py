import json
from django.shortcuts import render
from mapCreation.models import CarMapping, EndpointUsage
from django.conf import settings
from django.utils import timezone

def record_start_time(room_id):
    usage, created = EndpointUsage.objects.get_or_create(room_id=room_id, defaults={'start_time': timezone.now()})
    return usage.start_time


def car_mapping_visualization(request, room_id):
    if settings.DEMO_MODE:
        angle_data = [0, 45, 90, 135, 180]  # this and the distance data for testing
        distance_data = [10, 20, 30, 40, 50]  # the application without the node MCU
    else:
        start_time = record_start_time(room_id)
        car_mappings = CarMapping.objects.filter(timestamp__gte=start_time).order_by('timestamp')
        angle_data = [car_mapping.angle for car_mapping in car_mappings]
        distance_data = [car_mapping.distance for car_mapping in car_mappings]

    return render(request, 'visualization.html', {
        'room_id': room_id,
        'angle_data': json.dumps(angle_data),
        'distance_data': json.dumps(distance_data)
    })
