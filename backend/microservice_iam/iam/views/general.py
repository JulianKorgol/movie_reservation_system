from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.status import (
    HTTP_200_OK,
)
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema


@extend_schema(
    summary='Health Check',
    description='Check if the server is running.',
    tags=['v1'],
)
class HealthCheckView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    @extend_schema(auth=[])
    def get(self, req):
        return Response({
            'status': 'ok'
        }, status=HTTP_200_OK)
