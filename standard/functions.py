import json
from geopy.distance import geodesic
from standard.models.standard import Standard
from redis_connection import redis_connection
from shapely.geometry import Point, Polygon


def create_standards(user, company, min_acc=None, max_acc=None, min_velocity=None, max_velocity=None, in_tehran=None):
    Standard.objects.create(user=user,
                            company=company,
                            minimum_acceleration=min_acc,
                            maximum_acceleration=max_acc,
                            minimum_velocity=min_velocity,
                            maximum_velocity=max_velocity,
                            in_tehran=in_tehran)


def update_acceleration_standard(users, min_acc, max_acc):
    users.minimum_acceleration = min_acc
    users.maximum_acceleration = max_acc
    users.save()


def update_velocity_standard(users, min_velocity, max_velocity):
    users.minimum_acceleration = min_velocity
    users.maximum_acceleration = max_velocity
    users.save()


def update_is_tehran_standard(users: Standard, in_tehran):
    users.in_tehran = in_tehran
    users.save()


def update_standards(user, minimum_acceleration, maximum_acceleration, minimum_velocity, maximum_velocity, in_tehran):
    user.minimum_velocity = minimum_velocity
    user.maximum_velocity = maximum_velocity
    user.minimum_acceleration = minimum_acceleration
    user.maximum_acceleration = maximum_acceleration
    user.in_tehran = in_tehran
    user.save()


def catch_standards(user, minimum_acceleration, maximum_acceleration, minimum_velocity, maximum_velocity, in_tehran):
    data = {
        'user_id': user.pk,
        'minimum_acceleration': minimum_acceleration,
        'maximum_acceleration': maximum_acceleration,
        'minimum_velocity': minimum_velocity,
        'maximum_velocity': maximum_velocity,
        'in_tehran': bool(in_tehran)
    }
    json_data = json.dumps(data)
    redis_connection.set_key(f'user_{user.pk}', json_data)


def is_in_tehran_province(latitude, longitude):
    tehran_province_polygon_coords = [
        (51.3304, 35.5474),
        (51.5806, 35.5474),
        (51.5806, 35.8682),
        (51.3304, 35.8682)
    ]

    tehran_province_polygon = Polygon(tehran_province_polygon_coords)
    point = Point(longitude, latitude)
    return point.within(tehran_province_polygon)


def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).kilometers


def check_acceleration_standard(location_information, all_company_standards):
    for standards in all_company_standards:
        if int(location_information.acceleration) in range(standards.minimum_acceleration,
                                                           standards.maximum_acceleration + 1):
            return bool(True)
    return bool(False)


def check_velocity_standard(location_information, all_company_standards):
    for standards in all_company_standards:
        if int(location_information.speed) in range(standards.minimum_velocity, standards.maximum_velocity + 1):
            return bool(True)
    return bool(False)


def check_standards(location_information, all_company_standards):
    for standards in all_company_standards:
        if int(location_information.speed) in \
                range(standards.minimum_velocity, standards.maximum_velocity) and \
                int(location_information.acceleration) in \
                range(standards.minimum_acceleration, standards.maximum_acceleration) and \
                standards.in_tehran == \
                is_in_tehran_province(longitude=location_information.longitude, latitude=location_information.latitude):
            return standards.pk
    return -1
