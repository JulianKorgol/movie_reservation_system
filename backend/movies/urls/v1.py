from django.urls import path
from rest_framework import routers
from movies.views import general, reservation_process, user_account

router = routers.DefaultRouter()

urlpatterns = [
  path('health-check/', general.HealthCheckView.as_view()),
  path('reservation/countries', reservation_process.ReservationProcessCountrySelection.as_view()),
  path('reservation/cities', reservation_process.ReservationProcessCitySelection.as_view()),
  path('reservation/cinemas', reservation_process.ReservationProcessCinemaSelection.as_view()),
  path('reservation/showtimes', reservation_process.ReservationProcessShowtimeSelection.as_view()),
  path('user/login_with/password', user_account.UserAccountLoginWithPassword.as_view()),
  path('user/me', user_account.UserAccountAboutMe.as_view()),
  path('user/logout', user_account.UserAccountLogOut.as_view()),
]
