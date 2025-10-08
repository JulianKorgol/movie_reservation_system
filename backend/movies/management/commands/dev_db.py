from django.core.management.base import BaseCommand

from movies.models import Country, City, Cinema


class Command(BaseCommand):
  help = "Load database with development data"

  def handle(self, *args, **options):
    print("Loading development data")

    # App required data

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

    cinema_warsaw_third = Cinema.objects.create(
      name="Mokotów",
      city=city_poland_first,
      postal_code="00-008",
      street="mokotowska",
      street_number="3A",
      url="mokotow")
    cinema_warsaw_third.save()

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

    # END App required data
