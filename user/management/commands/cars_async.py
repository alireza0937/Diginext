import concurrent.futures
import time
from django.core.management.base import BaseCommand
from user.models import Company
from user.models import Car


class Command(BaseCommand):

    def create_task(self, company_id):
        Car.objects.create(company_id=company_id)

    def handle(self, *args, **options):
        try:
            company_cars: Company = Company.objects.filter(is_made=False).first()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for i in range(company_cars.number_of_cars):
                    executor.submit(self.create_task(company_id=company_cars), i)
                company_cars.is_made = True
                company_cars.save()

        except:
            pass


new_obj = Command()
while True:
    new_obj.handle()
    try:
        time.sleep(20)

    except KeyboardInterrupt:
        pass
