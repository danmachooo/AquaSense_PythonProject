from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'readings', views.WaterQualityReadingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('latest/', views.get_latest_reading, name='latest-reading'),
    path('historical/', views.get_historical_data, name='historical-data'),
    path('alerts/', views.get_alerts, name='alerts'),
] 