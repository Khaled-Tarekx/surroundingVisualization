from django.db import models

class Obstacle(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    angle = models.FloatField()
    distance = models.FloatField()
    x_position = models.FloatField()
    y_position = models.FloatField()

    class Meta:
        verbose_name = 'Obstacle'
        verbose_name_plural = 'Obstacles'

    def __str__(self):
        return f"Obstacle at ({self.x_position}, {self.y_position}), Angle: {self.angle}, Distance: {self.distance}"

class EndpointUsage(models.Model):
    room_id = models.CharField(max_length=100)
    start_time = models.DateTimeField()

    def __str__(self):
        return f"Room ID: {self.room_id}, Start Time: {self.start_time}"

class CarImage(models.Model):
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return f"Car Image: {self.image.url}"

class Car(models.Model):
    car_x = models.FloatField()
    car_y = models.FloatField()
    car_angle = models.FloatField(null=True, blank=True)
    car_image = models.ForeignKey(CarImage, on_delete=models.SET_NULL, null=True)
    surroundings = models.ForeignKey(Obstacle, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Position ({self.car_x}, {self.car_y}), Angle {self.car_angle}, Image: {self.car_image.image.url}"
