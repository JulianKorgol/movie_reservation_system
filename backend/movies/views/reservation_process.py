from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response

from movies.models import Country, City
from movies.lib.public_models import PublicCountry, PublicCity

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample, OpenApiParameter


@extend_schema(
  summary="Country List",
  description="List of countries with active cinemas",
  tags=["v1", "ReservationProcess"],
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


@extend_schema(
  summary="City List",
  description="List of cities from selected country",
  tags=["v1", "ReservationProcess"],
)
class ReservationProcessCitySelection(generics.GenericAPIView):
  permission_classes = [AllowAny]

  @extend_schema(auth=[],
                 parameters=[OpenApiParameter(
                   name="country_url",
                   type=OpenApiTypes.STR,
                   description="Selected country",
                   default="pl"
                 )],
                 responses={
                   200: OpenApiResponse(
                     response=OpenApiTypes.OBJECT,
                     description="OK - No error",
                     examples=[
                       OpenApiExample(
                         name="2 Cities",
                         value={
                           "cities": [
                             {
                               "name": "Bydgoszcz",
                               "country": 3,
                               "url": "bydgoszcz"
                             },
                             {
                               "name": "Pruszków",
                               "country": 3,
                               "url": "pruszków"
                             }
                           ]
                         }
                       ),
                       OpenApiExample(
                         name="None",
                         value={
                           "cities": []
                         }
                       )
                     ]
                   ),
                   404: OpenApiResponse(
                     response=OpenApiTypes.OBJECT,
                     examples=[
                       OpenApiExample(
                         name="Country not found",
                         value={
                           "error_code": 1
                         }
                       )
                     ]
                   )
                 })
  def get(self, req) -> Response:
    try:
      country = Country.objects.get(url=req.query_params.get("country_url"))
    except Country.DoesNotExist:
      return Response(data={"error_code": 1}, status=status.HTTP_404_NOT_FOUND)

    cities_from_country = City.objects.filter(country=country)

    cities = [
      PublicCity(name=c.name, country=c.country.id, url=c.url).model_dump()
      for c in cities_from_country
    ]

    return Response({"cities": cities}, status=status.HTTP_200_OK)
