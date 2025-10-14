from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from movies.serializers import UserAccountLoginSerializer
from movies.lib.check import is_super_admin, is_admin, check_if_user_is_active
from movies.models import Account

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

    user = User.objects.filter(email=email).first()
    if user is not None and user.check_password(password):
      if check_if_user_is_active(Account.objects.get(user=user)):
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
              "user": {
                "email": "xyz@example.com",
                "first_name": "John",
                "last_name": "Williams",
                "role": "User"
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
        "user": {
          "email": user.email,
          "first_name": user.account.first_name,
          "last_name": user.account.last_name,
          "role": user.account.role.name
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


@extend_schema(
  summary="User account special privileges info",
  description="Get user account special privileges info if user has special privileges.",
  tags=["v1", "User"]
)
class UserAccountPrivileges(generics.GenericAPIView):
  permission_classes = [IsAuthenticated]

  @extend_schema(
    responses={
      200: OpenApiResponse(
        response=OpenApiTypes.OBJECT,
        description="OK",
        examples=[
          OpenApiExample(
            name="Super Admin privileges",
            value={
              "privileges": {
                "is_super_admin": True
              }
            }
          ),
          OpenApiExample(
            name="Admin privileges",
            value={
              "privileges": {
                "is_admin": True
              }
            }
          ),
          OpenApiExample(
            name="User - no special privileges",
            value={
              "privileges": None
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
    account = Account.objects.filter(user=user).first()

    if not account:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    privileges = {}

    if is_super_admin(account):
      privileges["is_super_admin"] = True

    if is_admin(account):
      privileges["is_admin"] = True

    return Response({
      "privileges": privileges if privileges else None,
    }, status=status.HTTP_200_OK)
