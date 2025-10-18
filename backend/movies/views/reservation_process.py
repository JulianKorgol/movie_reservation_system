import datetime
from zoneinfo import ZoneInfo

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response

from django.utils import timezone

from movies.models import Country, City, Cinema, CinemaRoom, Showtime, Movie, CinemaRoomRow, CinemaRoomSeat, TicketType, \
  Reservation, ReservationTicket
from movies.lib.public_models import PublicCountry, PublicCity, PublicCinema
from movies.lib.logs import app_logger
from movies.lib.enum.timezone import TimeZone

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
                                 "title": "The Falcon and the Winter Soldier",
                                 "description": "zzz",
                                 "genre": {
                                   "name": "For Kids",
                                   "url": "for-kids"
                                 },
                                 "image_path": "zzz.jpg",
                                 "url": "falcon-and-winter"
                               },
                               "showtimes": [
                                 {
                                   "id": 7024,
                                   "start_date": "2025-10-14T17:30:00+02:00",
                                   "end_date": "2025-10-14T20:13:00+02:00"
                                 },
                                 {
                                   "id": 6840,
                                   "start_date": "2025-10-14T16:30:00+02:00",
                                   "end_date": "2025-10-14T18:55:00+02:00"
                                 }
                               ]
                             },
                             {
                               "movie": {
                                 "title": "John Wick: Chapter 4",
                                 "description": "zzz",
                                 "genre": {
                                   "name": "Action",
                                   "url": "action"
                                 },
                                 "image_path": "zzz.jpg",
                                 "url": "john-wick-4"
                               },
                               "showtimes": [
                                 {
                                   "id": 6878,
                                   "start_date": "2025-10-14T13:30:00+02:00",
                                   "end_date": "2025-10-14T15:54:00+02:00"
                                 },
                                 {
                                   "id": 6916,
                                   "start_date": "2025-10-14T20:45:00+02:00",
                                   "end_date": "2025-10-14T23:14:00+02:00"
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
                                 "genre": None,
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
        selected_date = datetime.datetime.strptime(req_par_date, "%Y-%m-%d").date()
      except ValueError:
        return Response({"error": "Parameter: date is in incorrect format", "error_code": 6},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

      if selected_date > datetime_now.date() + datetime.timedelta(
        days=7) or selected_date < datetime_now.date():
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
      day_end = timezone.make_aware(datetime.datetime.combine(selected_date, datetime.time.max))

      if selected_date > datetime_now.date():
        day_start = timezone.make_aware(datetime.datetime.combine(selected_date, datetime.time.min))
      else:
        day_start = timezone.make_aware(datetime.datetime.combine(selected_date, datetime_now.time()))

      showtimes = Showtime.objects.filter(
        cinema_room__in=cinema_rooms,
        start_date__gte=day_start,
        end_date__lte=day_end,
      )
    else:
      showtimes = Showtime.objects.filter(
        cinema_room__in=cinema_rooms,
        start_date__range=(datetime_now, datetime_now + datetime.timedelta(days=2))
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
          "genre": {
            "name": movie.genre.name,
            "url": movie.genre.url
          } if movie.genre else None,
          "image_path": movie.image_path,
          "url": movie.url
        },
        "showtimes": [
          {
            "id": showtime.id,
            "start_date": showtime.start_date.astimezone(ZoneInfo(TimeZone.poland.value)),
            "end_date": showtime.end_date.astimezone(ZoneInfo(TimeZone.poland.value)),
          }
          for showtime in showtimes if
          showtime.movie == movie and showtime.start_date > datetime_now
        ]
      }
      for movie in movies_from_showtimes
    ]

    return Response({"data": response}, status=status.HTTP_200_OK)


@extend_schema(
  summary="Showtime Data",
  description="All data needed to start seat selection process.",
  tags=["v1", "ReservationProcess"],
)
class ReservationProcessShowtimeData(generics.GenericAPIView):
  permission_classes = [AllowAny]

  @extend_schema(
    parameters=[OpenApiParameter(
      name="showtime_id",
      type=OpenApiTypes.INT,
      description="Selected showtime",
      required=True
    )],
    responses={
      200: OpenApiResponse(
        response=OpenApiTypes.OBJECT,
        examples=[OpenApiExample(
          name="OK",
          value={
            "cinema": {
              "name": "Złote Tarasy",
              "url": "zlote-tarasy"
            },
            "movie": {
              "title": "F1",
              "url": "f1"
            },
            "showtime": {
              "start_date": "2025-10-19T23:45:00+02:00",
              "end_date": "2025-10-20T03:22:00+02:00"
            },
            "cinema_room": {
              "name": "Room 2",
              "rows_and_seats": [
                {
                  "row_number": 1,
                  "seats": [
                    {
                      "id": 93141,
                      "seat_number": 1,
                      "is_available": True,
                      "ticket_type": 187
                    },
                    {
                      "id": 93148,
                      "seat_number": 2,
                      "is_available": False,
                      "ticket_type": 187
                    }
                  ]
                },
                {
                  "row_number": 2,
                  "seats": [
                    {
                      "id": 93155,
                      "seat_number": 1,
                      "is_available": False,
                      "ticket_type": 189
                    },
                    {
                      "id": 93156,
                      "seat_number": 2,
                      "is_available": True,
                      "ticket_type": 189
                    }
                  ]
                },
                {
                  "row_number": 3,
                  "seats": [
                    {
                      "id": 93169,
                      "seat_number": 1,
                      "is_available": True,
                      "ticket_type": 187
                    },
                    {
                      "id": 93176,
                      "seat_number": 2,
                      "is_available": True,
                      "ticket_type": 187
                    },
                    {
                      "id": 93177,
                      "seat_number": 3,
                      "is_available": False,
                      "ticket_type": 187
                    }
                  ]
                }
              ]
            },
            "ticket_types": [
              {
                "id": 187,
                "name": "Normal Ticket",
                "price": 27,
                "currency": "PLN",
                "primary_ticket": None,
                "discount_percentage": None
              },
              {
                "id": 188,
                "name": "Discounted Ticket",
                "price": None,
                "currency": "PLN",
                "primary_ticket": 187,
                "discount_percentage": 37
              },
              {
                "id": 189,
                "name": "VIP Ticket",
                "price": 40,
                "currency": "PLN",
                "primary_ticket": 187,
                "discount_percentage": None
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
            name="Missing showtime_id",
            value={"error": "Missing required parameter: showtime_id in int format", "error_code": 1},
          )
        ]
      ),
      404: OpenApiResponse(
        response=OpenApiTypes.OBJECT,
        examples=[
          OpenApiExample(
            name="Showtime not found",
            value={"error": "Showtime not found", "error_code": 2}
          )
        ]
      )
    }
  )
  def get(self, request) -> Response:
    showtime_id = request.query_params.get("showtime_id")
    if not showtime_id or not showtime_id.isdigit():
      return Response({"error": "Missing required parameter: showtime_id in int format", "error_code": 1},
                      status=status.HTTP_400_BAD_REQUEST)

    showtime = Showtime.objects.filter(id=showtime_id).first()
    if not showtime:
      return Response({"error": "Showtime not found", "error_code": 2}, status=status.HTTP_404_NOT_FOUND)

    cinema_room_rows = CinemaRoomRow.objects.filter(cinema_room=showtime.cinema_room)
    cinema_room_seats = CinemaRoomSeat.objects.filter(row__in=cinema_room_rows.values_list("id", flat=True))

    ticket_types = []
    ticket_type_primary_ticket = TicketType.objects.filter(
      id__in=cinema_room_seats.values_list("seat_type_id", flat=True), primary_ticket=None).first()
    ticket_types.append(ticket_type_primary_ticket)

    ticket_types_with_primary_ticket = TicketType.objects.filter(primary_ticket=ticket_type_primary_ticket)
    for ticket_type in ticket_types_with_primary_ticket:
      ticket_types.append(ticket_type)

    if not ticket_types:
      app_logger.error(
        f"No ticket types found for {showtime_id} (ReservationProcessShowtimeData; 3)"
      )
      return Response({"error_code": 3}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    already_reserved_seats = ReservationTicket.objects.filter(
      reservation__showtime=showtime
    ).values_list("cinema_room_seat_id", flat=True)

    return Response({
      "cinema": {
        "name": showtime.cinema_room.cinema.name,
        "url": showtime.cinema_room.cinema.url,
      },
      "movie": {
        "title": showtime.movie.title,
        "url": showtime.movie.url,
      },
      "showtime": {
        "start_date": showtime.start_date.astimezone(ZoneInfo(TimeZone.poland.value)),
        "end_date": showtime.end_date.astimezone(ZoneInfo(TimeZone.poland.value)),
      },
      "cinema_room": {
        "name": showtime.cinema_room.name,
        "rows_and_seats": [
          {
            "row_number": cinema_room_row.row_number,
            "seats": [
              {
                "id": cinema_room_seat.id,
                "seat_number": cinema_room_seat.seat_number,
                "is_available": (cinema_room_seat.status == 1) and (cinema_room_seat.id not in already_reserved_seats),
                "ticket_type": cinema_room_seat.seat_type.id,
              }
              for cinema_room_seat in cinema_room_seats if cinema_room_seat.row == cinema_room_row
            ]
          } for cinema_room_row in cinema_room_rows
        ]
      },
      "ticket_types": [
        {
          "id": ticket_type.id,
          "name": ticket_type.name,
          "price": ticket_type.price,
          "currency": ticket_type.currency,
          "primary_ticket": ticket_type.primary_ticket.id if ticket_type.primary_ticket else None,
          "discount_percentage": ticket_type.discount_percentage if ticket_type.discount_percentage else None,
        }
        for ticket_type in ticket_types
      ],
    }, status=status.HTTP_200_OK)
