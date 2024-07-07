from django.urls import path
from .consumers import CarMappingConsumer

websocket_urlpatterns = [
    path('ws/car_mapping/<int:room_id>/', CarMappingConsumer.as_asgi()),
]
