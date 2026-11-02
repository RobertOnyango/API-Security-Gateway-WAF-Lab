# Sample patient data

# List of dictionaries: Each dictionary is a key:valeu pair of patient dictinaries
_patients = [
    {"id": 1, "name": "Alex Morgan", "date_of_birth": "1985-04-12"},
    {"id": 2, "name": "Sam Taylor", "date_of_birth": "1992-09-03"},
]

# Function that returns all patients
def get_all_patients():
    return _patients

# Function that gets patient by ID
def get_patient_by_id(patient_id):
    return next(
        (patient for patient in _patients if patient["id"] == patient_id),
        None,
    )

# Function that adds a patient on memory
def add_patient(name, date_of_birth):
    next_id = max((patient["id"] for patient in _patients), default=0) + 1
    patient = {
        "id": next_id,
        "name": name,
        "date_of_birth": date_of_birth,
    }
    _patients.append(patient)
    return patient