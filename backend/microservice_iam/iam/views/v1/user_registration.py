import hmac
import logging
import secrets
import hashlib

from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from iam.serializers.input.v1.user_registration import UserRegistrationViewSerializer, \
    UserEmailConfirmationViewSerializer
from iam.models import UserDetails
from iam.rate_limiting.v1 import RegistrationRateThrottle, EmailConfirmationRateThrottle

User = get_user_model()
logger = logging.getLogger(__name__)


@extend_schema(
    summary='User Registration',
    description='User registration endpoint',
    tags=['v1'],
)
class UserRegistrationView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationViewSerializer
    throttle_classes = [RegistrationRateThrottle]

    @extend_schema(
        auth=[],
        responses={
            201: OpenApiResponse(
                response=OpenApiTypes.NONE,
                examples=[
                    OpenApiExample(
                        name="User Created"
                    )
                ]
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.NONE,
                examples=[
                    OpenApiExample(
                        name="E-mail address already taken by another account",
                    )
                ]
            ),
            500: OpenApiResponse(
                response=OpenApiTypes.NONE,
                examples=[
                    OpenApiExample(
                        name="Internal Server Error",
                    )
                ]
            )
        }
    )
    def post(self, req, *args, **kwargs):
        serializer = UserRegistrationViewSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email_confirmation_token = secrets.token_hex(128)

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    email=data['email'],
                    password=data['password']
                )

                UserDetails.objects.create(
                    user=user,
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email_confirmation_token=hashlib.sha256(email_confirmation_token.encode()).hexdigest(),
                    country="PL"  # TODO: Create automatic check for user country
                )
        except IntegrityError:
            logger.info("REGISTRATION_DUPLICATE_EMAIL_RACE,email=%s", data['email'])
            return Response(status=HTTP_400_BAD_REQUEST)
        except Exception:
            logger.critical("REGISTRATION_UNEXPECTED_ERROR", exc_info=True)
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

        logger.debug(
            "REGISTRATION_CONFIRMATION_TOKEN,email=%s,token=%s",
            user.email,
            email_confirmation_token,
        )
        # TODO: Send email confirmation

        return Response(status=HTTP_201_CREATED)


@extend_schema(
    summary='User Email Confirmation',
    description='User email confirmation endpoint',
    tags=['v1'],
)
class UserEmailConfirmationView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserEmailConfirmationViewSerializer
    throttle_classes = [EmailConfirmationRateThrottle]

    @extend_schema(
        auth=[],
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.NONE,
                examples=[
                    OpenApiExample(
                        name="E-mail address confirmed",
                    )
                ]
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.NONE,
                examples=[
                    OpenApiExample(
                        name="User with that email does not exist",
                    ),
                    OpenApiExample(
                        name="Email token do not match"
                    )
                ]
            )
        }
    )
    def post(self, req, *args, **kwargs):
        serializer = UserEmailConfirmationViewSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        with transaction.atomic():
            user = User.objects.select_for_update().filter(email=data['email']).first()
            if not user:
                return Response(status=HTTP_400_BAD_REQUEST)

            if not user.details.email_confirmation_token:
                return Response(status=HTTP_400_BAD_REQUEST)

            if not hmac.compare_digest(
                    user.details.email_confirmation_token,
                    hashlib.sha256(data['email_confirmation_token'].encode()).hexdigest(),
            ):
                return Response(status=HTTP_400_BAD_REQUEST)

            user.details.email_confirmation_token = None
            user.status = 1
            user.details.save()
            user.save()

        return Response(status=HTTP_200_OK)
