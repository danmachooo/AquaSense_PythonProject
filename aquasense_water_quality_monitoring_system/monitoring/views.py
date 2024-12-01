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

def get_water_quality_label(reading):
    # Updated thresholds for lettuce
    thresholds = {
        'pH': {'Excellent': (6.0, 6.5), 'Good': (5.5, 7.0), 'Fair': (5.0, 7.5), 'Poor': (0, 14)},
        'temp': {'Excellent': (18, 22), 'Good': (15, 25), 'Fair': (10, 30), 'Poor': (0, 100)},
        'DO': {'Excellent': (7, 8), 'Good': (6, 9), 'Fair': (5, 10), 'Poor': (0, 20)},
        'EC': {'Excellent': (1.5, 2.0), 'Good': (1.0, 2.5), 'Fair': (0.5, 3.0), 'Poor': (0, 10)},
        'turbidity': {'Excellent': (0, 2), 'Good': (2, 5), 'Fair': (5, 10), 'Poor': (10, 100)},
        'nitrogen': {'Excellent': (10, 20), 'Good': (5, 30), 'Fair': (2, 50), 'Poor': (0, 100)},
        'phosphorus': {'Excellent': (3, 6), 'Good': (2, 8), 'Fair': (1, 10), 'Poor': (0, 20)},
        'potassium': {'Excellent': (15, 30), 'Good': (10, 40), 'Fair': (5, 50), 'Poor': (0, 100)},
        'hardness': {'Excellent': (50, 100), 'Good': (30, 150), 'Fair': (20, 200), 'Poor': (0, 300)},
    }
    
    labels = []
    for param, ranges in thresholds.items():
        value = getattr(reading, param)
        for label, (min_val, max_val) in ranges.items():
            if min_val <= value <= max_val:
                labels.append(label)
                break
    
    # Determine overall label using a point system
    label_points = {'Excellent': 4, 'Good': 3, 'Fair': 2, 'Poor': 1}
    total_points = sum(label_points[label] for label in labels)
    avg_points = total_points / len(labels)
    
    if avg_points >= 3.5:
        return 'Excellent'
    elif avg_points >= 2.5:
        return 'Good'
    elif avg_points >= 1.5:
        return 'Fair'
    else:
        return 'Poor'


@api_view(['GET'])
def get_latest_reading(request):
    latest_reading = WaterQualityReading.objects.latest('timestamp')
    serializer = WaterQualityReadingSerializer(latest_reading)
    data = serializer.data
    data['water_quality_label'] = get_water_quality_label(latest_reading)
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
        'EC': (1.5, 2.5),
        'turbidity': (1, 5),
        'nitrogen': (10, 20),
        'phosphorus': (5, 8),
        'potassium': (100, 150),
        'hardness': (70, 150),
    }
    
    latest_reading = WaterQualityReading.objects.latest('timestamp')
    alerts = []
    
    for param, (min_val, max_val) in thresholds.items():
        value = getattr(latest_reading, param)
        if value < min_val or value > max_val:
            alerts.append(f"{param} is out of range: {value}")
    
    return Response({'alerts': alerts})