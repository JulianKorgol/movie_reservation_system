import datetime
from zoneinfo import ZoneInfo

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response

from django.utils import timezone

from movies.models import Country, City, Cinema, CinemaRoom, Showtime, Movie
from movies.lib.public_models import PublicCountry, PublicCity, PublicCinema
from movies.lib.logs import app_logger
from backend.settings import TIME_ZONE

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
                   default="pl",
                   required=True
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
                   default="warszawa",
                   required=True
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


@extend_schema(
  summary="Showtimes List",
  description="List of showtimes from selected cinema. The endpoint returns showtimes for up to two days ahead. Use server time and server timezone.",
  tags=["v1", "ReservationProcess"],
)
class ReservationProcessShowtimeSelection(generics.GenericAPIView):
  permission_classes = [AllowAny]

  @extend_schema(auth=[],
                 parameters=[OpenApiParameter(
                   name="cinema_url",
                   type=OpenApiTypes.STR,
                   description="Selected cinema",
                   default="zlote-tarasy",
                   required=True
                 ),
                   OpenApiParameter(
                     name="date",
                     type=OpenApiTypes.DATE,
                     description="Selected day to show showtimes",
                     required=False,
                     default=datetime.date.today()
                   )
                 ],
                 responses={
                   200: OpenApiResponse(
                     response=OpenApiTypes.OBJECT,
                     examples=[
                       OpenApiExample(
                         name="OK 1",
                         value={
                           "data": [
                             {
                               "movie": {
                                 "title": "F1",
                                 "description": "xxx",
                                 "genre_url": "thriller",
                                 "image_path": "xxx.jpg",
                                 "url": "f1"
                               },
                               "showtimes": [
                                 {
                                   "id": 2220,
                                   "start_date": "2025-10-13T14:30:00+02:00",
                                   "end_date": "2025-10-13T17:05:00+02:00"
                                 }
                               ]
                             },
                             {
                               "movie": {
                                 "title": "The Fantastic 4: First Steps",
                                 "description": "zzz",
                                 "genre_url": "thriller",
                                 "image_path": "zzz.jpg",
                                 "url": "fantastic-4"
                               },
                               "showtimes": [
                                 {
                                   "id": 2171,
                                   "start_date": "2025-10-12T22:00:00+02:00",
                                   "end_date": "2025-10-13T01:27:00+02:00"
                                 },
                                 {
                                   "id": 2241,
                                   "start_date": "2025-10-14T11:30:00+02:00",
                                   "end_date": "2025-10-14T15:09:00+02:00"
                                 },
                                 {
                                   "id": 2309,
                                   "start_date": "2025-10-13T20:15:00+02:00",
                                   "end_date": "2025-10-13T22:37:00+02:00"
                                 },
                                 {
                                   "id": 2204,
                                   "start_date": "2025-10-13T11:00:00+02:00",
                                   "end_date": "2025-10-13T14:05:00+02:00"
                                 },
                                 {
                                   "id": 2310,
                                   "start_date": "2025-10-12T20:00:00+02:00",
                                   "end_date": "2025-10-12T22:33:00+02:00"
                                 }
                               ]
                             }
                           ]
                         }
                       ), OpenApiExample(
                         name="OK 2 - None values",
                         value={
                           "data": [
                             {
                               "movie": {
                                 "title": "F1",
                                 "description": "xxx",
                                 "genre_url": None,
                                 "image_path": "xxx.jpg",
                                 "url": "f1"
                               },
                               "showtimes": [
                                 {
                                   "id": 2220,
                                   "start_date": "2025-10-13T14:30:00+02:00",
                                   "end_date": "2025-10-13T17:05:00+02:00"
                                 }
                               ]
                             }
                           ]
                         }
                       ), OpenApiExample(
                         name="OK 3 - No showtimes",
                         value={
                           "data": [
                             {
                               "movie": {
                                 "title": "The Falcon and the Winter Soldier",
                                 "description": "zzz",
                                 "genre_url": "action",
                                 "image_path": "zzz.jpg",
                                 "url": "falcon-and-winter"
                               },
                               "showtimes": [
                                 {
                                   "id": 2780,
                                   "start_date": "2025-10-12T20:15:00+02:00",
                                   "end_date": "2025-10-12T23:07:00+02:00"
                                 }
                               ]
                             },
                             {
                               "movie": {
                                 "title": "John Wick: Chapter 4",
                                 "description": "zzz",
                                 "genre_url": "action",
                                 "image_path": "zzz.jpg",
                                 "url": "john-wick-4"
                               },
                               "showtimes": []
                             }
                           ]
                         }
                       )
                     ]
                   ),
                   400: OpenApiResponse(
                     response=OpenApiTypes.OBJECT,
                     examples=[
                       OpenApiExample(
                         name="Missing cinema_url",
                         value={"error": "Missing required parameter: cinema_url", "error_code": 1}
                       )
                     ]
                   ),
                   404: OpenApiResponse(
                     response=OpenApiTypes.OBJECT,
                     examples=[
                       OpenApiExample(
                         name="Cinema not found",
                         value={"error": "Cinema not found", "error_code": 2}
                       ),
                       OpenApiExample(
                         name="Showtimes not found",
                         value={"error": "No showtimes found", "error_code": 3}
                       )
                     ]
                   ),
                   500: OpenApiResponse(
                     response=OpenApiTypes.OBJECT,
                     examples=[
                       OpenApiExample(
                         name="Cinema rooms not found",
                         value={"error_code": 4}
                       ),
                       OpenApiExample(
                         name="Showtimes not found",
                         value={"error_code": 5}
                       ),
                       OpenApiExample(
                         name="Movies not found",
                         value={"error_code": 8}
                       )
                     ]
                   ),
                   422: OpenApiResponse(
                     response=OpenApiTypes.OBJECT,
                     examples=[
                       OpenApiExample(
                         name="Incorrect format of date parameter",
                         value={"error": "Parameter: date is in incorrect format", "error_code": 6}
                       ),
                       OpenApiExample(
                         name="Date parameter is too far in the future",
                         value={
                           "error": "Parameter: date should not be more than 7 days in the future or date should not be in the past.",
                           "error_code": 7}
                       )
                     ]
                   )
                 }
                 )
  def get(self, req) -> Response:
    req_par_cinema_url = req.query_params.get("cinema_url")
    if not req_par_cinema_url:
      return Response({"error": "Missing required parameter: cinema_url", "error_code": 1},
                      status=status.HTTP_400_BAD_REQUEST)

    req_par_date = req.query_params.get("date")
    selected_date = None
    datetime_now = timezone.now()
    if req_par_date:
      try:
        selected_date = timezone.make_aware(datetime.datetime.strptime(req_par_date, "%Y-%m-%d"),
                                            timezone=datetime_now.tzinfo)
      except ValueError:
        return Response({"error": "Parameter: date is in incorrect format", "error_code": 6},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

      if selected_date.date() > datetime_now.date() + datetime.timedelta(
        days=7) or selected_date.date() < datetime_now.date():
        return Response(
          {"error": "Parameter: date should not be more than 7 days in the future or date should not be in the past.",
           "error_code": 7},
          status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    selected_cinema = Cinema.objects.filter(url=req_par_cinema_url).first()
    if not selected_cinema:
      return Response({"error": "Cinema not found", "error_code": 2}, status=status.HTTP_404_NOT_FOUND)

    cinema_rooms = CinemaRoom.objects.filter(cinema=selected_cinema)
    if not cinema_rooms.exists():
      app_logger.error(f"No cinema rooms: {selected_cinema.url} (ReservationProcessShowtimeSelection, 4)")
      return Response({"error_code": 4}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if selected_date:
      showtimes = Showtime.objects.filter(
        cinema_room__in=cinema_rooms,
        start_date__gte=datetime.datetime.combine(selected_date,
                                                  datetime.datetime.min.time() if selected_date.date() > datetime_now.date() else datetime_now.time()),
        end_date__lte=datetime.datetime.combine(selected_date, datetime.datetime.max.time())
      )
    else:
      showtimes = Showtime.objects.filter(
        cinema_room__in=cinema_rooms,
        start_date__range=(datetime_now,
                           datetime.datetime.combine(datetime_now.date() + datetime.timedelta(days=2),
                                                     datetime.datetime.max.time()))
      )
    if not showtimes.exists():
      return Response({"error": "No showtimes found", "error_code": 3}, status=status.HTTP_404_NOT_FOUND)

    movies_from_showtimes = Movie.objects.filter(id__in=showtimes.values_list("movie_id", flat=True))
    if not movies_from_showtimes.exists():
      app_logger.error(
        f"No movies found for {selected_cinema.url} in {selected_date} (ReservationProcessShowtimeSelection; 8)")
      return Response({"error_code": 8}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response = [
      {
        "movie": {
          "title": movie.title,
          "description": movie.description,
          "genre_url": movie.genre.url if movie.genre else None,
          "image_path": movie.image_path,
          "url": movie.url
        },
        "showtimes": [
          {
            "id": showtime.id,
            "start_date": showtime.start_date.astimezone(ZoneInfo(TIME_ZONE)),
            "end_date": showtime.end_date.astimezone(ZoneInfo(TIME_ZONE)),
          }
          for showtime in showtimes if
          showtime.movie == movie and showtime.start_date > datetime_now
        ]
      }
      for movie in movies_from_showtimes
    ]

    return Response({"data": response}, status=status.HTTP_200_OK)
