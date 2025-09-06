from django.urls import path
from rest_framework import routers
from movies.views import general

router = routers.DefaultRouter()

urlpatterns = [
    path('health-check/', general.HealthCheckView.as_view()),
]
