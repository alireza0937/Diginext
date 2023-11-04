from standard.models import Standard


def create_standards(user, min_acc=None, max_acc=None, min_velocity=None, max_velocity=None, in_tehran=None):
    Standard.objects.create(user=user,
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
