import json
import time
from datetime import datetime
from django.core.management.base import BaseCommand
from redis_connection import redis_connection
from report.models import CarLocation
from standard.functions import check_standards
from standard.models.location import Location
from standard.models.standard import Standard
from user.models import Car


class Command(BaseCommand):

    def handle(self, *args, **options):
        pubsub = redis_connection.create_pubsub()
        pubsub.subscribe('diginext')

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = message['data'].decode('utf-8')
                data2: dict = json.loads(data)
                location_id = data2.get('location')
                location_information = Location.objects.filter(pk=location_id).first()
                which_company = Car.objects.filter(id=location_information.car_id.pk).first()
                all_company_standards = Standard.objects.filter(company_id=which_company.company_id.pk).all()
                longitude = location_information.longitude
                latitude = location_information.latitude

                standards_check = check_standards(location_information=location_information,
                                                  all_company_standards=all_company_standards)

                CarLocation.objects.create(latitude=latitude,
                                           longitude=longitude,
                                           car=location_information.car_id.pk,
                                           st_id=standards_check,
                                           timestamp=datetime.now())


command_object = Command()
while True:
    command_object.handle()
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        pass
