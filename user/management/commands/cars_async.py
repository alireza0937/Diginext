import concurrent.futures
from django.core.management.base import BaseCommand
from user.models import Company, Car


class Command(BaseCommand):
    help = 'Create tasks using threads based on a number from the database'

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
