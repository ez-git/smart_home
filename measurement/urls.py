from django.urls import path

from measurement.views import SensorView, SensorDetailView, MeasurementView

urlpatterns = [
    path('sensors/', SensorView.as_view()),
    path('sensors/<id>/', SensorDetailView.as_view()),
    path('measurements/', MeasurementView.as_view()),
]
