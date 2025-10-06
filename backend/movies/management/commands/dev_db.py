from django.core.management.base import BaseCommand

from movies.models import Country, City


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

    # END App required data
