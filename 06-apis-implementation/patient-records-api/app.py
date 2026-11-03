from flask import Flask, jsonify
# Import Blueprint containing endpoints
from routes.patient_routes import patients_bp
#Initialize Flask
app = Flask(__name__)
#Register the blueprint
app.register_blueprint(patients_bp)

# Health check for endpoint
@app.get("/health")
def health():
    return jsonify({"status": "healthy", "service": "patient-records-api"}), 200