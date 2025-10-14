from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from movies.serializers import UserAccountLoginSerializer
from movies.lib.check import is_super_admin, is_admin

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample, OpenApiParameter


@extend_schema(
  summary="User account login",
  description="User account login endpoint",
  tags=["v1", "User"]
)
class UserAccountLoginWithPassword(generics.GenericAPIView):
  permission_classes = [AllowAny]
  serializer_class = UserAccountLoginSerializer

  @extend_schema(auth=[], responses={
    200: OpenApiResponse(
      response=OpenApiTypes.NONE,
      description="OK - login successful",
    ),
    400: OpenApiResponse(
      response=OpenApiTypes.OBJECT,
      description="Incorrect data",
      examples=[
        OpenApiExample(
          name="Incorrect data",
          value={"error": "Missing required data: email, password", "error_code": 1}
        )
      ]
    ),
    401: OpenApiResponse(
      response=OpenApiTypes.OBJECT,
      description="Invalid credentials",
      examples=[
        OpenApiExample(
          name="Incorrect credentials",
          value={"error": "Invalid credentials", "error_code": 2}
        )
      ]
    ),
    403: OpenApiResponse(
      response=OpenApiTypes.OBJECT,
      description="User is suspended",
      examples=[
        OpenApiExample(
          name="User is suspended",
          value={"error": "User is suspended", "error_code": 3}
        )
      ]
    )
  })
  def post(self, request) -> Response:
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
      return Response({"error": "Missing required data: email, password", "error_code": 1},
                      status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(email=email)
    if user.check_password(password):
      if user.is_active:
        login(request, user)
        return Response(status=status.HTTP_200_OK)
      else:
        return Response({"error": "User is suspended", "error_code": 3}, status=status.HTTP_403_FORBIDDEN)

    return Response({"error": "Invalid credentials", "error_code": 2}, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(
  summary="User account details endpoint",
  description="Get basic user account details",
  tags=["v1", "User"]
)
class UserAccountAboutMe(generics.GenericAPIView):
  permission_classes = [IsAuthenticated]

  @extend_schema(
    responses={
      200: OpenApiResponse(
        response=OpenApiTypes.OBJECT,
        description="OK - login successful",
        examples=[
          OpenApiExample(
            name="OK",
            value={
              "data": {
                "email": "example@example.com",
                "first_name": "John",
                "last_name": "XYZ",
                "role": {
                  "id": 3,
                  "name": "User"
                }
              },
              "privileges": {
                "is_super_admin": False,
                "is_admin": False
              }
            }
          )
        ]
      ),
      403: OpenApiResponse(
        response=OpenApiTypes.OBJECT,
        description="User not logged in",
        examples=[
          OpenApiExample(
            name="No credentials",
            value={
              "detail": "Authentication credentials were not provided."
            }
          )
        ]
      )
    }
  )
  def get(self, request) -> Response:
    user = request.user

    return Response(
      {
        "data": {
          "email": user.email,
          "first_name": user.account.first_name,
          "last_name": user.account.last_name,
          "role": {
            "id": user.account.role.id,
            "name": user.account.role.name
          }
        },
        "privileges": {
          "is_super_admin": is_super_admin(user.account),
          "is_admin": is_admin(user.account)
        }
      }, status=status.HTTP_200_OK
    )


@extend_schema(
  summary="User account logout",
  description="Sending request to this endpoint will logout user.",
  tags=["v1", "User"]
)
class UserAccountLogOut(generics.GenericAPIView):
  permission_classes = [IsAuthenticated]

  @extend_schema(
    responses={
      200: OpenApiResponse(
        response=OpenApiTypes.NONE,
        description="OK - logout successful",
      ),
      403: OpenApiResponse(
        response=OpenApiTypes.OBJECT,
        description="User not logged in",
        examples=[
          OpenApiExample(
            name="No credentials",
            value={
              "detail": "Authentication credentials were not provided."
            }
          )
        ]
      )
    }
  )
  def get(self, request) -> Response:
    logout(request)
    return Response(status=status.HTTP_200_OK)
