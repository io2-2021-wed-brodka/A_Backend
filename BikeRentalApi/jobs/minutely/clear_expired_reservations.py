from django.utils import timezone
from django_extensions.management.jobs import MinutelyJob

from BikeRentalApi.enums import BikeState
from BikeRentalApi.models import Reservation


class Job(MinutelyJob):
    help = "Periodic job for clearing expired reservations."

    def execute(self):
        date_now = timezone.now()

        for res in Reservation.objects.filter(expire_date__lt = date_now):
            bike = res.bike
            bike.bike_state = BikeState.Working
            bike.save()
            res.delete()

        print("Cleared expired reservations")
