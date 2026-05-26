from django.urls import path

from rest_framework import routers

from iam.views.v1 import general, user_registration

router = routers.DefaultRouter()
internal_endpoint_path = "internal/"

urlpatterns = [
    path('health-check/', general.HealthCheckView.as_view()),
    path('user/registration/', user_registration.UserRegistrationView.as_view()),
    path('user/email/confirmation/', user_registration.UserEmailConfirmationView.as_view()),
]
