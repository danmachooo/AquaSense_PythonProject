from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import WaterQualityReading
from .serializers import WaterQualityReadingSerializer
from django.utils import timezone
from datetime import timedelta

class WaterQualityReadingViewSet(viewsets.ModelViewSet):
    queryset = WaterQualityReading.objects.all().order_by('-timestamp')
    serializer_class = WaterQualityReadingSerializer

@api_view(['GET'])
def get_latest_reading(request):
    latest_reading = WaterQualityReading.objects.latest('timestamp')
    serializer = WaterQualityReadingSerializer(latest_reading)
    data = serializer.data
    return Response(data)

@api_view(['GET'])
def get_historical_data(request):
    days = int(request.query_params.get('days', 7))
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)
    readings = WaterQualityReading.objects.filter(timestamp__range=[start_date, end_date])
    serializer = WaterQualityReadingSerializer(readings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_alerts(request):
    # Define threshold values for each parameter
    thresholds = {
        'pH': (6.0, 7.0),
        'temp': (18, 24),
        'DO': (6, 8),
        'EC': (1.2, 1.8),
        'turbidity': (0, 5),
        'nitrogen': (100, 200),
        'phosphorus': (30, 50),
        'potassium': (150, 300),
        'hardness': (100, 200),
    }
    
    latest_reading = WaterQualityReading.objects.latest('timestamp')
    alerts = []
    
    for param, (min_val, max_val) in thresholds.items():
        value = getattr(latest_reading, param)
        if value < min_val or value > max_val:
            alerts.append(f"{param} is out of range: {value}")
    
    return Response({'alerts': alerts})