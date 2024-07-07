from django.db import models

class CarMapping(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    angle = models.IntegerField()
    distance = models.FloatField()

    class Meta:
        verbose_name = 'Car Mapping'
        verbose_name_plural = 'Car Mappings'

class EndpointUsage(models.Model):
    room_id = models.CharField(max_length=100)
    start_time = models.DateTimeField()

    def __str__(self):
        return f"Room ID: {self.room_id}, Start Time: {self.start_time}"
    