from rest_framework.authtoken.models import Token
from redis_connection import redis_connection
from report.models import CarLocation
from standard.functions import calculate_distance
from datetime import datetime, timedelta
from standard.models.standard import Standard
from user.models import Car, Company
from datetime import date
import json


class Reporting:
    def __init__(self, car_id):
        self.car_id = car_id
        self.cnt = 0

    @staticmethod
    def check_if_the_instance_is_none(instance):
        if instance is None:
            return 0
        response = json.loads(instance)
        return response

    def can_use_cache_or_not(self, start_date: date, end_date: date, standard_id):
        if end_date == datetime.today().date():
            return self._generate_report_data(start_date, end_date, standard_id)
        return self._read_from_cache(start_date, end_date, standard_id)

    @staticmethod
    def convert_date_type_to_datetime(start_date, end_date) -> (datetime, datetime):
        yearS, monthS, dayS = str(start_date).split('-')
        yearE, monthE, dayE = str(end_date).split('-')
        start_date = datetime(int(yearS), int(monthS), int(dayS))
        end_date = datetime(int(yearE), int(monthE), int(dayE))
        return start_date, end_date

    def check_car_existence(self):
        response = CarLocation.objects.filter(car=self.car_id).exists()
        if response:
            return True
        return False

    def _read_from_cache(self, start_date, end_date, standard_id=None):
        delta = (end_date - start_date)
        if standard_id is not None:
            mileage_base_standard = 0
            time_base_standard = 0
            for i in range(delta.days + 1):
                current_date = start_date + timedelta(days=i)
                date = current_date.strftime("%Y-%m-%d")
                mileage_response = self.check_if_the_instance_is_none(
                    (redis_connection.get_key(f'MileageBaseStandard-'
                                              f'CarID:{self.car_id}-'
                                              f'Date:{date}-'
                                              f'StandardID:{int(standard_id)}')))

                time_response = self.check_if_the_instance_is_none(
                    (redis_connection.get_key(f'TimeBaseStandard-'
                                              f'CarID:{self.car_id}-'
                                              f'Date:{date}-'
                                              f'StandardID:{int(standard_id)}')))
                mileage_base_standard += mileage_response

                time_base_standard += time_response

            standard_object = Standard.objects.filter(pk=standard_id).first()
            if time_base_standard == 0 and mileage_base_standard == 0 and self.cnt == 0:
                self.generate_and_cache_data(start_date, end_date, self.car_id)
                self.cnt += 1
                return self.can_use_cache_or_not(start_date=start_date, end_date=end_date, standard_id=standard_id)

            return {
                'Your Standard ID': int(standard_id),
                'Start Date': start_date,
                'End Date': end_date,
                'Car ID': self.car_id,
                'Standard Velocity Range': f"{standard_object.minimum_velocity} - {standard_object.maximum_velocity}",
                'Standard Acceleration Range': f"{standard_object.minimum_acceleration} - {standard_object.maximum_acceleration}",
                'OutSide Tehran': f"{standard_object.in_tehran}",
                'Mileage Base Standard': f"{round(mileage_base_standard, 2)} Km",
                'Time Base Standard': f"{round(time_base_standard, 2)} Min",

            }

        total_mileage = 0
        total_time = 0
        for i in range(delta.days + 1):
            current_date = start_date + timedelta(days=i)
            date = current_date.strftime("%Y-%m-%d")
            mileage_response = self.check_if_the_instance_is_none(redis_connection.get_key(key=f'TotalMileage-'
                                                                                               f'CarID:{self.car_id}-'
                                                                                               f'Date:{date}-'
                                                                                               f'StandardID:TotalMileage'))

            total_mileage += mileage_response

            time_response = self.check_if_the_instance_is_none(redis_connection.get_key(key=f'TotalTime-'
                                                                                            f'CarID:{self.car_id}-'
                                                                                            f'Date:{date}-'
                                                                                            f'StandardID:TotalTime'))

            total_time += time_response

            if total_time == 0 and total_mileage == 0 and self.cnt == 0:
                self.generate_and_cache_data(start_date, end_date, self.car_id)
                self.cnt += 1
                return self.can_use_cache_or_not(start_date=start_date, end_date=end_date, standard_id=standard_id)

        return {
            'Start Date': start_date,
            'End Date': end_date,
            'Car ID': self.car_id,
            'Total Mileage': f'{round(total_mileage, 2)} Km',
            'Total Time': f'{round(total_time, 2)} Min',

        }

    def company_member_check(self, token):
        try:
            user_id = Token.objects.get(key=token).user.id
        except:
            return False
        else:
            company_id = Company.objects.filter(user_id=user_id).first().pk
            is_company_user = Car.objects.filter(pk=self.car_id, company_id_id=company_id).exists()
            if is_company_user:
                return True
            return False

    def _get_filtered_locations(self, start_date, end_date):
        end_date = date(end_date.year, end_date.month, end_date.day + 1)
        return CarLocation.objects.filter(
            car=self.car_id, timestamp__gte=start_date, timestamp__lte=end_date)

    def _calculate_duration_in_minutes(self, start_location, end_location):
        duration = datetime.strptime(str(start_location.timestamp.time()), '%H:%M:%S.%f') - \
                   datetime.strptime(str(end_location.timestamp.time()), '%H:%M:%S.%f')
        return abs(duration.total_seconds() / 60)

    def calculate_mileage(self, start_date, end_date, standard_id=None):
        locations = self._get_filtered_locations(start_date, end_date)
        total_mileage = 0.0

        if standard_id is not None:
            for cnt in range(len(locations) - 1):
                if locations[cnt].st_id == int(standard_id) and locations[cnt + 1].st_id == int(standard_id):
                    distance = calculate_distance((locations[cnt].latitude, locations[cnt].longitude),
                                                  (locations[cnt + 1].latitude, locations[cnt + 1].longitude))

                    total_mileage += distance
            return total_mileage

        for cnt in range(len(locations) - 1):
            distance = calculate_distance((locations[cnt].latitude, locations[cnt].longitude),
                                          (locations[cnt + 1].latitude, locations[cnt + 1].longitude))
            total_mileage += distance

        return total_mileage

    def calculate_time(self, start_date, end_date, standard_id=None):

        locations = self._get_filtered_locations(start_date, end_date)

        total_minutes = 0
        if standard_id is not None:

            for cnt in range(len(locations) - 1):
                if locations[cnt].st_id == int(standard_id) and locations[cnt + 1].st_id == int(standard_id):
                    duration = self._calculate_duration_in_minutes(
                        start_location=locations[cnt], end_location=locations[cnt + 1])
                    total_minutes += duration
            return total_minutes

        for cnt in range(len(locations) - 1):
            duration = self._calculate_duration_in_minutes(
                start_location=locations[cnt], end_location=locations[cnt + 1])
            total_minutes += duration

        return total_minutes

    def _generate_report_data(self, start_time, end_time, standard_id=None):

        if standard_id is None:
            total_mileage = self.calculate_mileage(start_date=start_time, end_date=end_time)

            total_time = self.calculate_time(start_date=start_time, end_date=end_time)

            return {
                'Start Date': start_time,
                'End Date': end_time,
                'Car ID': self.car_id,
                'Total Mileage': f'{round(total_mileage, 2)} Km',
                'Total Time': f'{round(total_time, 2)} Min',

            }

        standard_object = Standard.objects.filter(pk=standard_id).first()

        mileage_base_standard = self.calculate_mileage(start_date=start_time, end_date=end_time,
                                                       standard_id=standard_id)

        time_base_standard = self.calculate_time(start_date=start_time, end_date=end_time,
                                                 standard_id=standard_id)

        return {
            'Your Standard ID': int(standard_id),
            'Start Date': start_time,
            'End Date': end_time,
            'Car ID': self.car_id,
            'Standard Velocity Range': f"{standard_object.minimum_velocity} - {standard_object.maximum_velocity}",
            'Standard Acceleration Range':
                f"{standard_object.minimum_acceleration} - {standard_object.maximum_acceleration}",
            'OutSide Tehran': f"{standard_object.in_tehran}",
            'Mileage Base Standard': f"{round(mileage_base_standard, 2)} Km",
            'Time Base Standard': f"{round(time_base_standard, 2)} Min",

        }

    def generate_and_cache_data(self, start_date, end_date, car_id):
        locations = self._get_filtered_locations(start_date=start_date, end_date=end_date).values_list('st_id',
                                                                                                       'car').distinct()
        for all_standards in locations:
            if all_standards[1] == int(car_id):
                if all_standards[0] != -1:
                    mileage_base_standard = self.calculate_mileage(start_date=start_date, end_date=end_date,
                                                                   standard_id=all_standards[0])

                    time_base_standard = self.calculate_time(start_date=start_date, end_date=end_date,
                                                             standard_id=all_standards[0])

                    redis_connection.set_key(
                        key=f'MileageBaseStandard-'
                            f'CarID:{car_id}-'
                            f'Date:{start_date}-'
                            f'StandardID:{all_standards[0]}',
                        value=mileage_base_standard)

                    redis_connection.set_key(
                        key=f'TimeBaseStandard-'
                            f'CarID:{car_id}-'
                            f'Date:{start_date}-'
                            f'StandardID:{all_standards[0]}',
                        value=time_base_standard)

                total_mileage = self.calculate_mileage(start_date=start_date, end_date=end_date)
                total_time = self.calculate_time(start_date=start_date, end_date=end_date)

                redis_connection.set_key(key=f'TotalMileage-'
                                             f'CarID:{car_id}-'
                                             f'Date:{start_date}-'
                                             f'StandardID:TotalMileage',
                                         value=total_mileage)

                redis_connection.set_key(key=f'TotalTime-'
                                             f'CarID:{car_id}-'
                                             f'Date:{start_date}-'
                                             f'StandardID:TotalTime',
                                         value=total_time)
