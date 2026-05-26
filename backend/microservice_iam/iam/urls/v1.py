from django.urls import path

from rest_framework import routers

from iam.views.v1 import general

router = routers.DefaultRouter()
internal_endpoint_path = "internal/"

urlpatterns = [
    path('health-check/', general.HealthCheckView.as_view()),
]
