from django.urls import path
from rest_framework import routers
from movies.views import general, reservation_process

router = routers.DefaultRouter()

urlpatterns = [
    path('health-check/', general.HealthCheckView.as_view()),
    path('reservation/countries', reservation_process.ReservationProcessCountrySelection.as_view()),
]
