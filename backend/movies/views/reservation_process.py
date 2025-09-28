from tkinter.scrolledtext import example

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response

from movies.models import Country
from movies.lib.public_models import PublicCountry

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample


@extend_schema(
    summary="Country List",
    description="List of countries with active cinemas",
    tags=["v1", "Country", "ReservationProcess"],
)
class ReservationProcessCountrySelection(generics.GenericAPIView):
    permission_classes = [AllowAny]

    @extend_schema(auth=[], responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="OK - No error",
            examples=[
                OpenApiExample(
                    name="1",
                    value={
                        "countries": [
                            {
                                "name": "Brazil",
                                "url": "xxx"
                            },
                            {
                                "name": "Spain",
                                "url": "zzz"
                            }
                        ]
                    }
                )
            ]
        )
    })
    def get(self, req) -> Response:
        countries_from_db = Country.objects.all()

        countries = [
            PublicCountry(name=country.name, url=country.url).model_dump()
            for country in countries_from_db
        ]

        return Response({"countries": countries}, status=status.HTTP_200_OK)
