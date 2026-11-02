from flask import Flask, jsonify

from routes.patient_routes import patients_bp

app = Flask(__name__)
app.register_blueprint(patients_bp)


@app.get("/health")
def health():
    return jsonify({"status": "healthy", "service": "patient-records-api"}), 200