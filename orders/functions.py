from sympy import im
from .models import Courier, CourierStatus
from django.core.exceptions import ObjectDoesNotExist


def get_order_status_from_courier_status(courier_status):
    try:
        courier_status_object = CourierStatus.objects.get(
            courier_status=courier_status)
        local_status = courier_status.local_status
        return local_status
    except ObjectDoesNotExist as e:
        print(e)
