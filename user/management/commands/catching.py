from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from report.models import CarLocation
from report.reporting_class import Reporting
import time


class Command(BaseCommand):

    def handle(self, *args, **options):
        today = datetime.now().date()
        end_of_day = datetime.combine(today, datetime.min.time()) + timedelta(days=1)
        all_cars = CarLocation.objects.all().values('car').distinct()
        for cars in all_cars:
            reporting_instance = Reporting(car_id=cars.get('car'))
            reporting_instance.generate_and_cache_data(start_date=today,
                                                       end_date=end_of_day,
                                                       car_id=int(cars.get('car')))


new_obj = Command()
while True:
    current_time = datetime.now().time()
    if current_time.hour == 23 and current_time.minute == 0:
        new_obj.handle()

        next_day = datetime.now() + timedelta(days=1)
        next_run_time = datetime(next_day.year, next_day.month, next_day.day, 23, 0)
        time_until_next_run = (next_run_time - datetime.now()).total_seconds()

        time.sleep(time_until_next_run)
    else:
        try:
            time.sleep(60)

        except KeyboardInterrupt:
            pass
