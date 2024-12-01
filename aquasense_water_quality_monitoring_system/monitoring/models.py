from django.db import models

class WaterQualityReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    pH = models.FloatField()
    temp = models.FloatField()
    DO = models.FloatField()
    EC = models.FloatField()
    turbidity = models.FloatField()
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    hardness = models.FloatField()
    label = models.CharField(max_length=50)

    def __str__(self):
        return f"Reading at {self.timestamp}"