import math
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from mapCreation.models import Car, CarImage, Obstacle


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
            car_x = data.get('car_x')
            car_y = data.get('car_y')
            car_angle = data.get('car_angle', 0) # if no car angle is given from the node mcu default the value to 0

            if angle is None or distance is None:
                await self.send_json({'error': 'Missing angle or distance'})
                return


            new_x, new_y = await self.get_object_position(car_x, car_y, car_angle, angle, distance)
            data['new_x'] = new_x
            data['new_y'] = new_y
            car_image = await CarImage.objects.first()
            car_image_url = car_image.image.url
            data['car_image_url'] = car_image_url

            await self.save_data_to_database(angle, distance, car_y, car_x, car_angle, car_image)
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
    def save_data_to_database(self, angle, distance, car_x, car_y, car_angle, car_image):
        car_1 = Car.objects.create(car_x=car_x, car_y=car_y, car_angle=car_angle, car_image=car_image)
        new_x, new_y = self.get_object_position(car_x, car_y, car_angle, angle, distance)
        car_2 = Car.objects.create(car_x=new_x, car_y=new_y, car_angle=car_angle, car_image=car_image)
        obstacle = Obstacle.objects.create(angle=angle, distance=distance, x_position=new_x, y_position=new_y)
        return car_1, car_2, obstacle

    async def car_mapping_update(self, event):
        await self.send_json(event['data'])
