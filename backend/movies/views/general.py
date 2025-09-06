from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework import generics
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema


@extend_schema(
    summary='Health Check',
    description='Check if the server is running.',
    tags=['v1_General'],
)
class HealthCheckView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    @extend_schema(auth=[])
    def get(self, req):
        return Response({
            'status': 'ok'
        }, status=HTTP_200_OK)
