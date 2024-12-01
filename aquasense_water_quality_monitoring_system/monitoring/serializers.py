from rest_framework import serializers
from .models import WaterQualityReading

class WaterQualityReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterQualityReading
        fields = '__all__'