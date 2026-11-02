from flask import Flask, jsonify
from routes.appointment_routes import appointments_bp

app = Flask(__name__)
app.register_blueprint(appointments_bp)

@app.get("/health")
def health():
    return jsonify({"status": "healthy", "service": "appointments-api"}), 200

"""
Testing the API endpoing health locally:

In the terminal, run: `python -m flask --app .\06-apis-implementation\appointments-api\app.py run`

Then open `http://127.0.0.1:5000/health` in your terminal. You should see the JSON payload above.

"""



