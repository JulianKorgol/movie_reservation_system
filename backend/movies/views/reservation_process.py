from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response

from movies.models import Country, City, Cinema
from movies.lib.public_models import PublicCountry, PublicCity, PublicCinema

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
                   ),
                   400: OpenApiResponse(
                     response=OpenApiTypes.OBJECT,
                     examples=[
                       OpenApiExample(
                         name="Missing country_url",
                         value={
                           "error": "Missing required parameter: country_url",
                           "error_code": 2
                         }
                       )
                     ]
                   )
                 })
  def get(self, req) -> Response:
    if not req.query_params.get("country_url"):
      return Response(data={"error": "Missing required parameter: country_url", "error_code": 2},
                      status=status.HTTP_400_BAD_REQUEST)

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


@extend_schema(
  summary="Cinema List",
  description="List of cinemas from selected city",
  tags=["v1", "ReservationProcess"],
)
class ReservationProcessCinemaSelection(generics.GenericAPIView):
  permission_classes = [AllowAny]

  @extend_schema(auth=[],
                 parameters=[OpenApiParameter(
                   name="city_url",
                   type=OpenApiTypes.STR,
                   description="Selected city",
                   default="warszawa"
                 )],
                 responses={
                   200: OpenApiResponse(
                     response=OpenApiTypes.OBJECT,
                     examples=[
                       OpenApiExample(
                         name="1 Cinema",
                         value={
                           "cinemas": [
                             {
                               "name": "Bonarka",
                               "city": 12,
                               "postal_code": "30-415",
                               "street": "Kamieńskiego",
                               "street_number": "11",
                               "url": "bonarka"
                             }
                           ]
                         }
                       ),
                       OpenApiExample(
                         name="None",
                         value={
                           "cinemas": []
                         }
                       )
                     ]
                   ),
                   400: OpenApiResponse(
                     response=OpenApiTypes.OBJECT,
                     examples=[
                       OpenApiExample(
                         name="Missing city_url",
                         value={"error": "Missing required parameter: city_url", "error_code": 1}
                       )
                     ]
                   ),
                   404: OpenApiResponse(
                     response=OpenApiTypes.OBJECT,
                     examples=[
                       OpenApiExample(
                         name="City not found",
                         value={
                           "error": "City not found",
                           "error_code": 2
                         }
                       )
                     ]
                   )
                 }
                 )
  def get(self, req) -> Response:
    req_par_city_url = req.query_params.get("city_url")
    if not req_par_city_url:
      return Response(data={"error": "Missing required parameter: city_url", "error_code": 1},
                      status=status.HTTP_400_BAD_REQUEST)

    try:
      selected_city = City.objects.get(url=req_par_city_url)
    except City.DoesNotExist:
      return Response(data={"error": "City not found", "error_code": 2},
                      status=status.HTTP_404_NOT_FOUND)

    cinemas_from_city = Cinema.objects.filter(city=selected_city)

    cinemas = [
      PublicCinema(
        name=cinema.name,
        city=cinema.city.id,
        postal_code=cinema.postal_code,
        street=cinema.street,
        street_number=cinema.street_number,
        url=cinema.url
      ).model_dump()
      for cinema in cinemas_from_city
    ]

    return Response(data={"cinemas": cinemas}, status=status.HTTP_200_OK)
