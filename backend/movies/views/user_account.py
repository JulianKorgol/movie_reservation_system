from django.contrib.auth import authenticate, login

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from movies.serializers import UserAccountLoginSerializer

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample, OpenApiParameter


class UserAccountLogin(generics.GenericAPIView):
  permission_classes = [AllowAny]
  serializer_class = UserAccountLoginSerializer

  def post(self, request) -> Response:
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
      return Response({"error": "Missing required data: email, password", "error_code": 1},
                      status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(email=email, password=password)
    if user:
      if user.is_active:
        login(request, user)
        return Response(status=status.HTTP_200_OK)
      else:
        return Response({"error": "User is suspended", "error_code": 3}, status=status.HTTP_403_FORBIDDEN)

    return Response({"error": "Invalid credentials", "error_code": 2}, status=status.HTTP_401_UNAUTHORIZED)
