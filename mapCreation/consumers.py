import math
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from mapCreation.models import CarMapping


class CarMappingConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = 'car_mapping'
        self.room_group_name = f'room_{self.scope["url_route"]["kwargs"]["room_id"]}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        try:
            data = content.get('data', {})
            if not data:
                await self.send_json({'error': 'Invalid data'})
                return

            angle = data.get('angle')
            distance = data.get('distance')

            if angle is None or distance is None:
                await self.send_json({'error': 'Missing angle or distance'})
                return

            car_x = 0
            car_y = 0
            new_x, new_y = self.get_object_position(car_x, car_y, angle, distance, car_angle=0)
            data['new_x'] = new_x
            data['new_y'] = new_y

            await self.save_data_to_database(angle, distance)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'car_mapping_update',
                    'data': data
                }
            )
        except Exception as e:
            await self.send_json({'error': str(e)})

    @staticmethod
    async def get_object_position(car_x, car_y, car_angle, distance, angle):
        total_angle = (car_angle + angle) % 360
        angle_rad = total_angle * (math.pi / 180)
        new_x = car_x + distance * math.cos(angle_rad)
        new_y = car_y + distance * math.sin(angle_rad)
        return new_x, new_y

    @database_sync_to_async
    def save_data_to_database(self, angle, distance):
        CarMapping.objects.create(angle=angle, distance=distance)

    async def car_mapping_update(self, event):
        await self.send_json(event['data'])
