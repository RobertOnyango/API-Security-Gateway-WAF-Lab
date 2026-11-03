# Sample appointments data repo
_appointments = [
    {"id": 1, "patient_id": 1, "date": "2026-11-10T09:00:00Z", "status": "scheduled"},
    {"id": 2, "patient_id": 2, "date": "2026-11-11T14:30:00Z", "status": "scheduled"},
]

# Get all appointments
def get_all_appointments():
    return _appointments

# Single appointment lookup
def get_appointment_by_id(appointment_id):
    return next(
        (appointment for appointment in _appointments if appointment["id"] == appointment_id),
        None,
    )