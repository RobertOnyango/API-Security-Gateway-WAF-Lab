# Code that cordinates the application operations
from repositories.patient_repository import get_all_patients, get_patient_by_id, add_patient

# Separation of duties: Service function that calls the get_all_patients function
def list_patients():
    return get_all_patients()


def get_patient(patient_id):
    return get_patient_by_id(patient_id)

def create_patient(name, date_of_birth):
    return add_patient(name, date_of_birth)