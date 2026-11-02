from flask import Blueprint, jsonify, request

from services.patient_service import list_patients, get_patient, create_patient

patients_bp = Blueprint("patients", __name__)

# Get the ful list of patients
@patients_bp.get("/patients")
def get_patients():
    return jsonify(list_patients())

# Get patients by valid IDs only. 200 success, 404 if not available in repo
@patients_bp.get("/patients/<int:patient_id>")
def get_patient_by_id_route(patient_id):
    patient = get_patient(patient_id)
    if patient is None:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify(patient), 200

@patients_bp.post("/patients")
def create_patient_route():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    name = payload.get("name")
    date_of_birth = payload.get("date_of_birth")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "name is required"}), 400
    if not isinstance(date_of_birth, str) or not date_of_birth.strip():
        return jsonify({"error": "date_of_birth is required"}), 400

    patient = create_patient(name.strip(), date_of_birth.strip())
    return jsonify(patient), 201