import random
import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User

from movies.models import Role, Country, City, Cinema, Movie, MovieGenre, CinemaRoom, CinemaRoomRow, CinemaRoomSeat, \
  TicketType, Showtime, Account


class Command(BaseCommand):
  help = "Load database with development data"

  def handle(self, *args, **options):
    print("Loading development data...")

    # ***User Roles***
    Role.objects.all().delete()

    role_super_admin = Role.objects.create(id=1, name="Super Admin")
    role_admin = Role.objects.create(id=2, name="Admin")
    role_user = Role.objects.create(id=3, name="User")

    # ***END User Roles***

    # ***User / Account ***
    Account.objects.all().delete()
    User.objects.all().delete()

    user_super_admin = User.objects.create(
      username="super_admin",
      email="super_admin@example.com",
    )
    user_super_admin.set_password("1234567890")
    user_super_admin_account = Account.objects.create(
      user=user_super_admin,
      role=role_super_admin,
      first_name="Alice",
      last_name="Johnson",
    )

    user_admin = User.objects.create(
      username="admin",
      email="admin@example.com",
    )
    user_admin.set_password("qwerty")
    user_admin_account = Account.objects.create(
      user=user_admin,
      role=role_admin,
      first_name="Michael",
      last_name="Smith",
    )

    user_first = User.objects.create(
      username="user_first",
      email="user_first@example.com",
    )
    user_first.set_password('1234')
    user_first_account = Account.objects.create(
      user=user_first,
      role=role_user,
      first_name="Sophia",
      last_name="Williams",
    )

    # *** END User / Account ***

    # ***Country***
    Country.objects.all().delete()

    country_first = Country.objects.create(name="Poland", url="pl")
    country_first.save()

    country_second = Country.objects.create(name="United States", url="usa")
    country_second.save()
    # ***END Country***

    # ***Cities***

    City.objects.all().delete()

    city_poland_first = City.objects.create(name="Warszawa", country=country_first, url="warszawa")
    city_poland_first.save()

    city_poland_second = City.objects.create(name="Kraków", country=country_first, url="krakow")
    city_poland_second.save()

    city_poland_third = City.objects.create(name="Lublin", country=country_first, url="lublin")
    city_poland_third.save()

    city_usa_first = City.objects.create(name="New York", country=country_second, url="new-york")
    city_usa_first.save()

    city_usa_second = City.objects.create(name="San Diego", country=country_second, url="san-diego")
    city_usa_second.save()

    # ***END Cities***

    # ***Ticket Types***
    TicketType.objects.all().delete()

    ticket_type_poland_normal = TicketType.objects.create(
      country=country_first,
      name="Normal Ticket",
      price=27.00,
      currency="PLN"
    )

    ticket_type_poland_discounted = TicketType.objects.create(
      country=country_first,
      name="Discounted Ticket",
      currency="PLN",
      primary_ticket=ticket_type_poland_normal,
      discount_percentage=37.00
    )

    ticket_type_poland_vip = TicketType.objects.create(
      country=country_first,
      name="Discounted Ticket",
      price=Decimal("40.00"),
      currency="PLN",
      primary_ticket=ticket_type_poland_normal,
    )

    # ***END Ticket Types)

    # ***Cinemas***
    Cinema.objects.all().delete()

    cinema_warsaw_first = Cinema.objects.create(
      name="Złote Tarasy",
      city=city_poland_first,
      postal_code="00-001",
      street="Złota",
      street_number="3A",
      url="zlote-tarasy")
    cinema_warsaw_first.save()

    cinema_warsaw_second = Cinema.objects.create(
      name="Arkadia",
      city=city_poland_first,
      postal_code="00-003",
      street="arkadiowa",
      street_number="7A",
      url="arkadia")
    cinema_warsaw_second.save()

    # cinema_warsaw_third = Cinema.objects.create(
    #   name="Mokotów",
    #   city=city_poland_first,
    #   postal_code="00-008",
    #   street="mokotowska",
    #   street_number="3A",
    #   url="mokotow")
    # cinema_warsaw_third.save()

    cinema_krakow_first = Cinema.objects.create(
      name="Bonarka",
      city=city_poland_second,
      postal_code="30-415",
      street="Kamieńskiego",
      street_number="11",
      url="bonarka"
    )
    cinema_krakow_first.save()

    cinema_lublin_first = Cinema.objects.create(
      name="Plaza Lublin",
      city=city_poland_third,
      postal_code="20-029",
      street="Lipowa",
      street_number="13",
      url="plaza-lublin"
    )
    cinema_lublin_first.save()

    cinema_newyork_first = Cinema.objects.create(
      name="AMC Empire 25",
      city=city_usa_first,
      postal_code="10036",
      street="W 42nd St",
      street_number="234",
      url="amc-empire-25"
    )
    cinema_newyork_first.save()

    cinema_sandiego_first = Cinema.objects.create(
      name="Landmark Hillcrest",
      city=city_usa_second,
      postal_code="92103",
      street="University Ave",
      street_number="3965",
      url="landmark-hillcrest"
    )
    cinema_sandiego_first.save()

    # ***END Cinemas***

    # ***Movies***
    MovieGenre.objects.all().delete()
    Movie.objects.all().delete()

    movie_genre_thriller = MovieGenre.objects.create(name="Thriller", url="thriller")
    movie_genre_thriller.save()

    movie_genre_action = MovieGenre.objects.create(name="Action", url="action")
    movie_genre_action.save()

    movie_genre_kids = MovieGenre.objects.create(name="For Kids", url="for-kids")
    movie_genre_kids.save()

    movie_f1 = Movie.objects.create(
      title="F1",
      description="xxx",
      genre=movie_genre_thriller,
      image_path="xxx.jpg",
      url="f1"
    )
    movie_f1.save()

    movie_fantastic4 = Movie.objects.create(
      title="The Fantastic 4: First Steps",
      description="zzz",
      genre=movie_genre_thriller,
      image_path="zzz.jpg",
      url="fantastic-4"
    )
    movie_fantastic4.save()

    movie_falcon_and_winter = Movie.objects.create(
      title="The Falcon and the Winter Soldier",
      description="zzz",
      genre=movie_genre_action,
      image_path="zzz.jpg",
      url="falcon-and-winter"
    )
    movie_falcon_and_winter.save()

    movie_john_wick_4 = Movie.objects.create(
      title="John Wick: Chapter 4",
      description="zzz",
      genre=movie_genre_action,
      image_path="zzz.jpg",
      url="john-wick-4"
    )
    movie_john_wick_4.save()

    # ***END Movies***

    # ***Cinema Rooms / Seats***
    CinemaRoom.objects.all().delete()
    CinemaRoomRow.objects.all().delete()
    CinemaRoomSeat.objects.all().delete()

    def generate_seats_for_room(cinema_room: CinemaRoom,
                                number_of_seats_per_row: int,
                                number_of_normal_rows: int,
                                number_of_vip_rows: int,
                                number_of_normal_seats_after_vip_seats: int,
                                ticket_type_normal: TicketType,
                                ticket_type_vip: TicketType,
                                ) -> None:
      # Normal rows
      for row in range(1, number_of_normal_rows + 1):
        temp_row = CinemaRoomRow.objects.create(
          row_number=row,
          cinema_room=cinema_room,
        )

        for seat in range(1, number_of_seats_per_row + 1):
          CinemaRoomSeat.objects.create(
            row=temp_row,
            seat_number=seat,
            seat_type=ticket_type_normal,
          )

      # VIP rows
      for row in range(number_of_normal_rows + 1, number_of_normal_rows + number_of_vip_rows + 1):
        temp_row = CinemaRoomRow.objects.create(
          row_number=row,
          cinema_room=cinema_room,
        )

        for seat in range(1, number_of_seats_per_row + 1):
          CinemaRoomSeat.objects.create(
            row=temp_row,
            seat_number=seat,
            seat_type=ticket_type_vip,
          )

      # Normal rows
      for row in range(number_of_normal_rows + number_of_vip_rows + 1,
                       number_of_normal_rows + number_of_vip_rows + number_of_normal_seats_after_vip_seats + 1):
        temp_row = CinemaRoomRow.objects.create(
          row_number=row,
          cinema_room=cinema_room,
        )

        for seat in range(1, number_of_seats_per_row + 1):
          CinemaRoomSeat.objects.create(
            row=temp_row,
            seat_number=seat,
            seat_type=ticket_type_normal
          )

    room_first = CinemaRoom.objects.create(
      name="Room 1",
      cinema=cinema_warsaw_first,
    )
    generate_seats_for_room(
      cinema_room=room_first,
      number_of_seats_per_row=10,
      number_of_normal_rows=5,
      number_of_vip_rows=2,
      number_of_normal_seats_after_vip_seats=3,
      ticket_type_normal=ticket_type_poland_normal,
      ticket_type_vip=ticket_type_poland_vip
    )

    room_second = CinemaRoom.objects.create(
      name="Room 2",
      cinema=cinema_warsaw_first,
    )
    generate_seats_for_room(
      cinema_room=room_second,
      number_of_seats_per_row=14,
      number_of_normal_rows=11,
      number_of_vip_rows=2,
      number_of_normal_seats_after_vip_seats=4,
      ticket_type_normal=ticket_type_poland_normal,
      ticket_type_vip=ticket_type_poland_vip
    )

    room_third = CinemaRoom.objects.create(
      name="Room 3",
      cinema=cinema_warsaw_first,
    )
    generate_seats_for_room(
      cinema_room=room_third,
      number_of_seats_per_row=10,
      number_of_normal_rows=5,
      number_of_vip_rows=1,
      number_of_normal_seats_after_vip_seats=3,
      ticket_type_normal=ticket_type_poland_normal,
      ticket_type_vip=ticket_type_poland_vip
    )

    room_waw2_first = CinemaRoom.objects.create(
      name="Room 1",
      cinema=cinema_warsaw_second,
    )
    generate_seats_for_room(
      cinema_room=room_first,
      number_of_seats_per_row=10,
      number_of_normal_rows=6,
      number_of_vip_rows=1,
      number_of_normal_seats_after_vip_seats=3,
      ticket_type_normal=ticket_type_poland_normal,
      ticket_type_vip=ticket_type_poland_vip
    )

    room_waw2_second = CinemaRoom.objects.create(
      name="Room 2",
      cinema=cinema_warsaw_second,
    )
    generate_seats_for_room(
      cinema_room=room_second,
      number_of_seats_per_row=14,
      number_of_normal_rows=10,
      number_of_vip_rows=1,
      number_of_normal_seats_after_vip_seats=4,
      ticket_type_normal=ticket_type_poland_normal,
      ticket_type_vip=ticket_type_poland_vip
    )

    room_waw2_third = CinemaRoom.objects.create(
      name="Room 3",
      cinema=cinema_warsaw_second,
    )
    generate_seats_for_room(
      cinema_room=room_third,
      number_of_seats_per_row=10,
      number_of_normal_rows=4,
      number_of_vip_rows=3,
      number_of_normal_seats_after_vip_seats=3,
      ticket_type_normal=ticket_type_poland_normal,
      ticket_type_vip=ticket_type_poland_vip
    )

    room_fourth = CinemaRoom.objects.create(
      name="Room 1",
      cinema=cinema_lublin_first,
    )
    generate_seats_for_room(
      cinema_room=room_second,
      number_of_seats_per_row=14,
      number_of_normal_rows=11,
      number_of_vip_rows=2,
      number_of_normal_seats_after_vip_seats=4,
      ticket_type_normal=ticket_type_poland_normal,
      ticket_type_vip=ticket_type_poland_vip
    )

    room_fifth = CinemaRoom.objects.create(
      name="Room 2",
      cinema=cinema_lublin_first,
    )
    generate_seats_for_room(
      cinema_room=room_fifth,
      number_of_seats_per_row=9,
      number_of_normal_rows=7,
      number_of_vip_rows=2,
      number_of_normal_seats_after_vip_seats=4,
      ticket_type_normal=ticket_type_poland_normal,
      ticket_type_vip=ticket_type_poland_vip
    )

    room_sixth = CinemaRoom.objects.create(
      name="Room 1",
      cinema=cinema_krakow_first,
    )
    generate_seats_for_room(
      cinema_room=room_sixth,
      number_of_seats_per_row=14,
      number_of_normal_rows=11,
      number_of_vip_rows=2,
      number_of_normal_seats_after_vip_seats=4,
      ticket_type_normal=ticket_type_poland_normal,
      ticket_type_vip=ticket_type_poland_vip
    )

    room_seven = CinemaRoom.objects.create(
      name="Room 2",
      cinema=cinema_krakow_first,
    )
    generate_seats_for_room(
      cinema_room=room_seven,
      number_of_seats_per_row=9,
      number_of_normal_rows=7,
      number_of_vip_rows=2,
      number_of_normal_seats_after_vip_seats=4,
      ticket_type_normal=ticket_type_poland_normal,
      ticket_type_vip=ticket_type_poland_vip
    )

    # ***END Cinema Rooms / Seats***

    # ***Showtimes***
    Showtime.objects.all().delete()

    start_date = timezone.make_aware(datetime.datetime.now())
    end_date = start_date + datetime.timedelta(days=7)
    for i in range(250):
      for _ in range(10):
        random_number_of_day = random.randint(0, (end_date - start_date).days)
        date = start_date + datetime.timedelta(days=random_number_of_day)

        hour = random.randint(10, 22)
        minute = random.choice([0, 15, 30, 45])
        start_time = timezone.make_aware(datetime.datetime(date.year, date.month, date.day, hour, minute))

        duration = random.randint(120, 240)
        end_time = start_time + datetime.timedelta(minutes=duration)

        in_for_movie = random.choice([movie_f1, movie_fantastic4, movie_falcon_and_winter, movie_john_wick_4])
        in_for_room = random.choice(
          [room_first, room_second, room_third, room_waw2_first, room_waw2_second, room_waw2_third, room_third,
           room_fourth, room_fifth, room_sixth, room_seven])

        # Check for time conflicts
        conflict_exists = Showtime.objects.filter(
          cinema_room=in_for_room,
        ).filter(
          Q(start_date__lt=end_time) & Q(end_date__gt=start_time)
        ).exists()

        if not conflict_exists:
          Showtime.objects.create(
            movie=in_for_movie,
            start_date=start_time,
            end_date=end_time,
            cinema_room=in_for_room
          )
          break

    # ***END Showtimes***

    print("Loading development data finished!")
