# Coordinate the applications activities
from repositories.appointment_repository import get_all_appointments, get_appointment_by_id


def list_appointments():
    return get_all_appointments()

def get_appointment(appointment_id):
    return get_appointment_by_id(appointment_id)