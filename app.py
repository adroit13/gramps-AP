from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all API routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@app.route("/")
def home():
    return "GrampsWeb API is running!"

@app.route("/api/metadata/")
def metadata():
    return jsonify({"status": "success", "message": "API metadata available"})

# ✅ FIX: Allow POST requests on this endpoint
@app.route("/api/translations/en", methods=["POST", "OPTIONS"])
def translations():
    if request.method == "OPTIONS":
        return '', 204  # ✅ Handle CORS preflight request
    return jsonify({"message": "Translation data received", "status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
