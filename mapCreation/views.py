import json
from django.shortcuts import render
from mapCreation.models import Car, Obstacle, EndpointUsage
from django.conf import settings
from django.utils import timezone
from django.templatetags.static import static

def record_start_time(room_id):
    usage, created = EndpointUsage.objects.get_or_create(room_id=room_id, defaults={'start_time': timezone.now()})
    return usage.start_time

def car_mapping_visualization(request, room_id):
    if settings.DEMO_MODE:
        angle_data = [0, 45, 90, 180, 270, 360]
        distance_data = [10, 20, 30, 40, 50, 60]
        car_x = 200
        car_y = 200
        car_angle = 45
        car_image_url = static('images/car_image_url.png')
    else:
        start_time = record_start_time(room_id)
        obstacles = Obstacle.objects.filter(timestamp__gte=start_time).order_by('timestamp')
        angle_data = [obstacle.angle for obstacle in obstacles]
        distance_data = [obstacle.distance for obstacle in obstacles]
        car = Car.objects.filter(timestamp__gte=start_time).order_by('timestamp')
        if car:
            car_x = car.car_x
            car_y = car.car_y
            car_angle = car.car_angle
            car_image = car.car_image
            if car_image:
                car_image_url = car_image.image.url
            else:
                car_image_url = static('images/car_image_url.png')
        else:
            car_x = 300
            car_y = 300
            car_angle = 0
            car_image_url = static('images/car_image_url.png')

    return render(request, 'visualization.html', {
        'room_id': room_id,
        'angle_data': json.dumps(angle_data),
        'distance_data': json.dumps(distance_data),
        'car_x': car_x,
        'car_y': car_y,
        'car_angle': car_angle,
        'car_image_url': car_image_url,
    })
