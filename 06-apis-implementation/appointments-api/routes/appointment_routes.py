from flask import Blueprint, jsonify

from services.appointment_service import list_appointments, get_appointment

appointments_bp = Blueprint("appointments", __name__)


@appointments_bp.get("/appointments")
def get_appointments():
    return jsonify(list_appointments())

@appointments_bp.get("/appointments/<int:appointment_id>")
def get_appointment_by_id_route(appointment_id):
    appointment = get_appointment(appointment_id)
    if appointment is None:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify(appointment), 200