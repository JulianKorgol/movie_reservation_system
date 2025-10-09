from django.db import models
from django.contrib.auth.models import User

import uuid as lib_uuid

'''
Auth Models
'''


class Role(models.Model):
  name = models.CharField(max_length=100)


class Account(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  role = models.ForeignKey(Role, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=100, null=True, blank=True)
  last_name = models.CharField(max_length=100, null=True, blank=True)
  status = models.IntegerField(default=1)  # 0: banned, 1: active, 2: e-mail not activated


'''
END Auth Models
'''

'''
General Models
'''


class Country(models.Model):
  name = models.CharField(max_length=100)
  url = models.CharField(max_length=100)


class City(models.Model):
  name = models.CharField(max_length=100)
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  url = models.CharField(max_length=100)


class TicketType(models.Model):
  country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
  name = models.CharField(max_length=100)
  price = models.FloatField(null=True, blank=True)
  currency = models.CharField(max_length=100)
  primary_ticket = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
  discount_percentage = models.FloatField(null=True, blank=True)


'''
END General Models
'''

'''
Cinema Models
'''


class Cinema(models.Model):
  name = models.CharField(max_length=100, null=True, blank=True)
  city = models.ForeignKey(City, on_delete=models.CASCADE)
  postal_code = models.CharField(max_length=20)
  street = models.CharField(max_length=100)
  street_number = models.CharField(max_length=20)
  url = models.CharField(max_length=100)


class CinemaRoom(models.Model):
  name = models.CharField(max_length=100)
  status = models.IntegerField(default=1)  # 0: Broken, 1: Working
  cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)


class CinemaRoomRow(models.Model):
  cinema_room = models.ForeignKey(CinemaRoom, on_delete=models.CASCADE)
  row_number = models.IntegerField()


class CinemaRoomSeat(models.Model):
  row = models.ForeignKey(CinemaRoomRow, on_delete=models.CASCADE)
  seat_number = models.IntegerField()
  status = models.IntegerField(default=1)  # 0: Broken, 1: Working
  seat_type = models.ForeignKey(TicketType, on_delete=models.SET_NULL, null=True)


'''
END Cinema Models
'''

'''
Showtime and Movie Management Models
'''


class MovieGenre(models.Model):
  name = models.CharField(max_length=100)
  url = models.CharField(max_length=100)


class Movie(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)
  genre = models.ForeignKey(MovieGenre, on_delete=models.SET_NULL, null=True)
  image_path = models.CharField(max_length=255, null=True, blank=True)
  url = models.CharField(max_length=255, unique=True)


class Showtime(models.Model):
  movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  cinema_room = models.ForeignKey(CinemaRoom, on_delete=models.SET_NULL, null=True)


'''
END Showtime and Movie Management Models
'''

'''
Reservation Managment Models
'''


class Reservation(models.Model):
  account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
  showtime = models.ForeignKey(Showtime, on_delete=models.SET_NULL, null=True)
  status = models.IntegerField(default=3)  # 1: Confirmed, 2: Cancelled, 3: In Progress
  token = models.CharField(max_length=255, unique=True, null=True, blank=True)
  first_name = models.CharField(max_length=100, null=True, blank=True)  # For customers without account
  last_name = models.CharField(max_length=100, null=True, blank=True)  # For customers without account
  email = models.EmailField(null=True, blank=True)  # For customers without account
  payment_status = models.IntegerField(default=2)  # 1: Paid, 2: Unpaid, 3: Does not require payment, 4: Refunded
  payment_stripe_id = models.CharField(max_length=255, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)


class ReservationTicket(models.Model):
  uuid = models.UUIDField(primary_key=True, default=lib_uuid.uuid4)
  secret = models.UUIDField(default=lib_uuid.uuid4)
  reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True)
  cinema_room_seat = models.ForeignKey(CinemaRoomSeat, on_delete=models.SET_NULL, null=True, blank=True)
  ticket_type = models.ForeignKey(TicketType, on_delete=models.SET_NULL, null=True, blank=True)


'''
END Reservation Managment Models
'''
