from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False,
                            unique=True)
    description = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.name}'


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor,
                               related_name='measurements',
                               on_delete=models.CASCADE)
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sensor} - {self.temperature}'
