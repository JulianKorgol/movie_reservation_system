from django.core.management.base import BaseCommand
from movies.models import Country


class Command(BaseCommand):
    help = "Load database with development data"

    def handle(self, *args, **options):
        print("Loading development data")

        # App required data

        # ***Country***
        Country.objects.all().delete()

        country_first = Country.objects.create(name="Poland", url="pl")
        country_first.save()

        country_second = Country.objects.create(name="USA", url="usa")
        country_second.save()
        # ***END Country***

        # END App required data
